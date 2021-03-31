import sys
import os
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import time
import psycopg2
from helpers import get_config
from dotenv import load_dotenv
import helpers
from db_helpers import *
from helpers import *
import logging
import custom_logger
import click
import pandas as pd

from tabulate import tabulate
import json
from datetime import datetime
import pprint
import boto3

pp = pprint.PrettyPrinter(indent=4)

env_path = current_path / "../../../../.env"
shared_path = current_path / "../../../shared"
sql_path = shared_path / "sql"
sql_path_temp = sql_path / "temp"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
config = get_config(environment)

# logging
log = logging.getLogger("root")
log.addHandler(custom_logger.MyHandler())
config.custom_log_level()
verbosity_levels = config.verbosity_levels

is_staging = False
conn_target = None
target_schema = None
source_schema = config.schemas["pre_transform"]
mapping_dict = None

mappings_to_run = [
    "bonds",
    "cases",
    "client_addresses",
    "client_persons",
    "client_phonenumbers"
]

results_sqlfile = "get_validation_results.sql"
validation_sqlfile = "validation.sql"
transformations_sqlfile = "transformation_functions.sql"
total_exceptions_sqlfile = "get_exceptions_total.sql"
host = os.environ.get("DB_HOST")
ci = os.getenv("CI")
bucket_name = f"casrec-migration-{environment.lower()}"
account = os.environ["SIRIUS_ACCOUNT"]
session = boto3.session.Session()
sql_lines = []


def set_logging_level(verbose):
    try:
        log.setLevel(verbosity_levels[verbose])
    except KeyError:
        log.setLevel("INFO")
        log.info(f"{verbose} is not a valid verbosity level")


def get_validation_dict():
    file_path = shared_path / "validation_mapping.json"
    validation_dict = json.load(open(file_path))
    return validation_dict


def get_mapping_report_df():
    file_path = shared_path / "mapping_definitions/summary/mapping_progress_summary.json"
    summary_dict = json.load(open(file_path))

    mappings = []
    for worksheet, worksheet_summary in summary_dict["worksheets"].items():
        if worksheet in mappings_to_run:
            mappings.append([worksheet] + list(worksheet_summary.values()))

    return pd.DataFrame.from_records(
        mappings, columns=["mapping", "rows", "unmapped", "mapped", "complete"]
    )


def get_exception_table(mapping_name):
    return f"{source_schema}.exceptions_{mapping_name}"


def drop_exception_tables():
    # drop all possible exception tables from last run
    for mapfile in helpers.get_all_mapped_fields().keys():
        sql_add(
    f"DROP TABLE IF EXISTS {get_exception_table(mapfile)};"
    )
    sql_add("")


def build_exception_table(mapping_name):
    exclude_cols = validation_dict[mapping_name]['exclude'] + list(validation_dict[mapping_name]['orderby'].keys())

    sql_add(f"-- {mapping_name}")
    sql_add(f"CREATE TABLE {get_exception_table(mapping_name)}(")
    sql_add("caserecnumber text default NULL,", 1)

    # overridden cols (normally run through plsql transform routines)
    for col in validation_dict[mapping_name]['overriden']:
        sql_add(f"{col} text default NULL,", 1)

    # forced order cols
    for col in list(validation_dict[mapping_name]['orderby'].keys()):
        sql_add(f"{col} text default NULL,", 1)

    # other columns
    separator = ",\n"
    sql_add(separator.join(
        [
            f"    {col} text default NULL"
            for col in mapping_dict.keys() if col not in exclude_cols
        ]
    ))
    sql_add(");", 0, 2)


def build_lookup_functions():
    # drop all the lookup tables from last run
    for lookup_name, lookup in helpers.get_all_lookup_dicts().items():
        sql_add(f"DROP FUNCTION IF EXISTS {source_schema}.{lookup_name}(character varying);")
    sql_add("")

    for lookup_name, lookup in helpers.get_all_lookup_dicts().items():
        sql_add(
            f"CREATE OR REPLACE FUNCTION {source_schema}.{lookup_name}(lookup_key varchar default null) RETURNS TEXT AS"
        )
        sql_add(f"$$")
        sql_add(f"SELECT CASE", 1)
        for k, v in lookup.items():
            try:
                sirius_value = v["sirius_mapping"].replace("'", "''")
            except AttributeError:
                sirius_value = v["sirius_mapping"]
            sql_add(f"WHEN ($1 = '{k}') THEN '{sirius_value}'", 2)
        sql_add("END", 1)
        sql_add("$$ LANGUAGE sql;", 0, 2)
    sql_add("")


def get_wrapped_sirius_col(col, mapped_item):
    sql = col
    col_definition = get_col_definition(mapped_item)
    if "current_date" == col_definition["transform_casrec"]["calculated"]:
        sql = f"CAST({col} AS DATE)"
    return sql


def get_sirius_col_name(mapped_item):
    col_definition = get_col_definition(mapped_item)
    col_table = col_definition["sirius_details"]["table_name"]
    mapped_item_name = mapped_item
    if isinstance(mapped_item, dict):
        if mapped_item["mapping_table"]:
            mapped_item_name = mapped_item["mapping_table"].split('.')[1]
    return f"{col_table}.{mapped_item_name}"


def sirius_wrap(mapped_item):
    col = get_sirius_col_name(mapped_item)
    col = get_wrapped_sirius_col(col, mapped_item)
    return col


def get_wrapped_casrec_col(col, mapped_item):
    col_definition = get_col_definition(mapped_item)
    datatype = col_definition["sirius_details"]["data_type"]
    calculated = col_definition["transform_casrec"]["calculated"]

    if datatype not in ["bool", "int"]:
        col = f"NULLIF(TRIM({col}), '')"

        if datatype in ["date"]:
            col = f"CAST(NULLIF(NULLIF(TRIM({col}), 'NaT'), '') AS DATE)"
        elif datatype in ["datetime"]:
            if "current_date" == calculated:
                col = f"CAST(NULLIF(TRIM({col}), '') AS DATE)"
            else:
                col = (
                    f"CAST(NULLIF(NULLIF(TRIM({col}), 'NaT'), '') AS TIMESTAMP(0))"
                )

    return col


def get_casrec_column_name(mapped_item):
    col_definition = get_col_definition(mapped_item)
    casrec_col_table = col_definition["transform_casrec"]["casrec_table"].lower()
    casrec_col_name = col_definition["transform_casrec"]["casrec_column_name"]
    return f'{source_schema}.{casrec_col_table}."{casrec_col_name}"'


def get_casrec_default_value(mapped_item):
    default_value = mapping_dict[mapped_item]["transform_casrec"]["default_value"]
    data_type = mapping_dict[mapped_item]["sirius_details"]["data_type"]

    if data_type in ["date", "datetime", "str"]:
        default_value = f"'{default_value}'"
    elif data_type == 'bool':
        default_value = default_value in ["true", "True", 1]

    return default_value


def get_casrec_calculated_value(mapped_item):
    callables = {
        "current_date": "'"
        + datetime.now().strftime("%Y-%m-%d")
        + "'"  # just do today's date
    }
    return callables.get(mapping_dict[mapped_item]["transform_casrec"]["calculated"])


def get_col_definition(mapped_item):
    if isinstance(mapped_item, dict) and "mapping_table" in mapped_item:
        pieces = mapped_item["mapping_table"].split('.')
        col_mapping = helpers.get_mapping_dict(
            file_name=pieces[0] + "_mapping", only_complete_fields=True, include_pk=False
        )
        col_definition = col_mapping[pieces[1]]
    else:
        col_definition = mapping_dict[mapped_item]

    return col_definition


def get_casrec_col_source(mapped_item):
    col = ''
    col_definition = get_col_definition(mapped_item)
    col_definition = col_definition["transform_casrec"]
    if col_definition["casrec_table"]:
        col = get_casrec_column_name(mapped_item)
        if "" != col_definition["lookup_table"]:
            db_lookup_func = col_definition["lookup_table"]
            col = f"{source_schema}.{db_lookup_func}({col})"
    elif "" != col_definition["default_value"]:
        col = get_casrec_default_value(mapped_item)
    elif "" != col_definition["calculated"]:
        col = get_casrec_calculated_value(mapped_item)

    if "" != col_definition["requires_transformation"]:
        transform_func = col_definition["requires_transformation"]
        col = f"transf_{transform_func}({col})"

    return col


def casrec_wrap(mapped_item):
    col = get_casrec_col_source(mapped_item)
    col = get_wrapped_casrec_col(col, mapped_item)
    return col


def build_validation_statements(mapping_name):
    casrec_overridden_cols = validation_dict[mapping_name]['casrec']['overriden']
    sirius_overridden_cols = validation_dict[mapping_name]['sirius']['overriden']
    exclude_cols = validation_dict[mapping_name]['exclude'] + list(validation_dict[mapping_name]['orderby'].keys())
    order_by = ",\n        ".join(['caserecnumber ASC'] + list(validation_dict[mapping_name]['orderby'].keys()))
    col_separator = ",\n"

    sql_add(f"INSERT INTO {get_exception_table(mapping_name)}(")

    # CASREC half
    sql_add("SELECT * FROM(", 1)
    sql_add("SELECT DISTINCT", 2)
    sql_add("pat.\"Case\" AS caserecnumber,", 3)

    # overridden cols (normally run through plsql transform routines)
    for colname, col in casrec_overridden_cols.items():
        sql_add(f"{col} AS {colname},", 3)

    # forced order cols
    for order_mapped_item_name, order_mapped_item in validation_dict[mapping_name]['orderby'].items():
        sql_add(f"{casrec_wrap(order_mapped_item)} AS {order_mapped_item_name},", 3)

    # standard cols
    sql_add(col_separator.join(
        [
            f"            {casrec_wrap(mapped_item)} AS {mapped_item}"
            for mapped_item in mapping_dict.keys() if mapped_item not in exclude_cols
        ]
    ))

    # FROM, with JOINs
    sql_add(f"FROM {source_schema}.{validation_dict[mapping_name]['casrec']['from_table']}", 2)
    for join in validation_dict[mapping_name]['casrec']['joins']:
        sql_add(f"{join}", 2)

    # WHERE
    sql_add("WHERE pat.\"Case\" IS NOT NULL", 2)
    for where_clause in validation_dict[mapping_name]['casrec']['where_clauses']:
        sql_add(f"AND {where_clause}", 2)

    # ORDER
    sql_add(f"ORDER BY {order_by}", 2)
    sql_add(") as csv_data", 1)
    sql_add("EXCEPT", 1)

    # SIRIUS half
    sql_add("SELECT * FROM(", 1)
    sql_add("SELECT DISTINCT", 2)

    #caserec col
    sql_add(f"persons.caserecnumber AS caserecnumber,", 3)

    # overridden cols (normally run through plsql transform routines)
    for colname, col in sirius_overridden_cols.items():
        sql_add(f"{col} AS {colname},", 3)

    # forced order cols
    for order_mapped_item_name, order_mapped_item in validation_dict[mapping_name]['orderby'].items():
        sql_add(f"{sirius_wrap(order_mapped_item)} AS {order_mapped_item_name},", 3)

    # standard cols
    sql_add(col_separator.join(
        [
            f"            {sirius_wrap(mapped_item)} AS {mapped_item}"
            for mapped_item in mapping_dict.keys() if mapped_item not in exclude_cols
        ]
    ))

    # FROM, with JOINs
    sql_add(f"FROM {target_schema}.{validation_dict[mapping_name]['sirius']['from_table']}", 2)
    for join in validation_dict[mapping_name]['sirius']['joins']:
        sql_add(f"{join}", 2)

    # WHERE
    sql_add("WHERE clientsource = 'CASRECMIGRATION'", 2)
    for where_clause in validation_dict[mapping_name]['sirius']['where_clauses']:
        sql_add(f"AND {where_clause}", 2)

    # ORDER
    sql_add(f"ORDER BY {order_by}", 2)
    sql_add(") as sirius_data", 1)
    sql_add(");", 0, 2)


def sql_add(sql, indent_level=0, line_breaks=1):
    global sql_lines
    indent = "    " * indent_level
    breaks = "\n" * line_breaks
    sql_lines.append(f"{indent}{sql}{breaks}")


def write_column_validation_sql(mapping_name, mapped_item, col_source_casrec, col_source_sirius):
    order_by = ",\n        ".join(['caserecnumber ASC'] + list(validation_dict[mapping_name]['orderby'].keys()))

    sql_add(f"-- {mapping_name} / {mapped_item}")
    sql_add(f"UPDATE {get_exception_table(mapping_name)}")
    sql_add(f"SET vary_columns = array_append(vary_columns, '{mapped_item}')")
    sql_add("WHERE caserecnumber IN (")
    sql_add(f"SELECT caserecnumber FROM (", 1)

    # casrec half
    sql_add("SELECT * FROM(", 2)
    sql_add("SELECT", 3)
    sql_add("exc_table.caserecnumber,", 4) # caserecnumber
    # forced order cols
    for order_mapped_item_name, order_mapped_item in validation_dict[mapping_name]['orderby'].items():
        sql_add(f"{casrec_wrap(order_mapped_item)} AS {order_mapped_item_name},", 4)
    # tested column
    sql_add(f"{col_source_casrec} AS {mapped_item}", 4)
    sql_add(f"FROM {source_schema}.{validation_dict[mapping_name]['casrec']['from_table']}", 3)
    for join in validation_dict[mapping_name]['casrec']['joins']:
        sql_add(f"{join}", 3)
    sql_add(f"LEFT JOIN {get_exception_table(mapping_name)} exc_table", 3)
    sql_add('ON exc_table.caserecnumber = pat."Case"', 4)
    # WHERE
    sql_add("WHERE exc_table.caserecnumber IS NOT NULL", 3)
    for where_clause in validation_dict[mapping_name]['casrec']['where_clauses']:
        sql_add(f"AND {where_clause}", 2)
    sql_add(f"ORDER BY {order_by}", 2)
    sql_add(") as csv_data", 2)

    sql_add("EXCEPT", 2)

    # sirius half
    sql_add("SELECT * FROM(", 2)
    sql_add("SELECT", 3)
    sql_add("exc_table.caserecnumber,", 4) # caserecnumber
    # forced order cols
    for order_mapped_item_name, order_mapped_item in validation_dict[mapping_name]['orderby'].items():
        sql_add(f"{sirius_wrap(order_mapped_item)} AS {order_mapped_item_name},", 4)
    # tested column
    sql_add(f"{col_source_sirius} AS {mapped_item}", 4)
    sql_add(f"FROM {target_schema}.{validation_dict[mapping_name]['sirius']['from_table']}", 3)
    for join in validation_dict[mapping_name]['sirius']['joins']:
        sql_add(f"{join}", 3)
    sql_add(f"LEFT JOIN {get_exception_table(mapping_name)} exc_table", 3)
    sql_add("ON exc_table.caserecnumber = persons.caserecnumber", 4)
    # WHERE
    sql_add("WHERE exc_table.caserecnumber IS NOT NULL", 3)
    for where_clause in validation_dict[mapping_name]['sirius']['where_clauses']:
        sql_add(f"AND {where_clause}", 2)
    sql_add(f"ORDER BY {order_by}", 2)
    sql_add(") as sirius_data", 2)

    sql_add(") as vary", 1)
    sql_add(");", 0, 2)


def build_column_validation_statements(mapping_name):
    sql_add(f"ALTER TABLE {get_exception_table(mapping_name)} DROP COLUMN IF EXISTS vary_columns;")
    sql_add(f"ALTER TABLE {get_exception_table(mapping_name)} ADD vary_columns varchar(255)[];", 0, 2)

    # test overridden columns
    for overridden_col in validation_dict[mapping_name]['overriden']:
        write_column_validation_sql(
            mapping_name,
            overridden_col,
            validation_dict[mapping_name]['casrec']['overriden'][overridden_col],
            validation_dict[mapping_name]['sirius']['overriden'][overridden_col]
        )

    # test regular columns
    for mapped_item in mapping_dict.keys():
        if mapped_item not in validation_dict[mapping_name]['exclude']:
            write_column_validation_sql(
                mapping_name,
                mapped_item,
                casrec_wrap(mapped_item),
                sirius_wrap(mapped_item)
            )


def write_validation_sql():
    global sql_lines
    log.debug(f"Writing to file")
    validation_sql_path = sql_path_temp / validation_sqlfile
    validation_sql_file = open(validation_sql_path, "w")
    validation_sql_file.writelines(sql_lines)
    validation_sql_file.close()
    log.debug(f"Saved to file: {validation_sql_path}")


def write_results_sql():
    sql_file = open(sql_path_temp / results_sqlfile, "w")
    results_rows = []
    for mapping in mappings_to_run:
        casrec_table_name = validation_dict[mapping]['casrec']['from_table']
        results_rows.append(
            f"SELECT '{mapping}' AS mapping,\n"
            f"(SELECT COUNT(*) FROM {source_schema}.{casrec_table_name}) as attempted,\n"
            f"(SELECT COUNT(*) FROM {get_exception_table(mapping)}),\n"
            f"(SELECT CONCAT( CAST( CAST( (\n"
            f"    (SELECT COUNT(*) FROM {get_exception_table(mapping)}) / \n"
            f"    (SELECT COUNT(*) FROM {source_schema}.{casrec_table_name})::FLOAT) * 100 AS NUMERIC) AS TEXT), '%')),\n"
            f"CAST((SELECT json_agg(vary) AS affected_columns FROM (\n"
            f"    SELECT DISTINCT unnest(vary_columns) as vary FROM {get_exception_table(mapping)}\n"
            f") t1) AS TEXT)\n"
        )
    separator = "UNION\n"
    sql_file.writelines(separator.join(results_rows))
    sql_file.close()


def write_get_exception_count_sql():
    sql_file = open(sql_path_temp / total_exceptions_sqlfile, "w")
    sql = f"SELECT SUM(exceptions) FROM (\n"

    ex_tables_sql = []
    for mapping in mappings_to_run:
        ex_tables_sql.append(
            f"    SELECT COUNT(*) as exceptions, 'client_persons' "
            f"FROM {get_exception_table(mapping)}\n"
        )

    separator = "    UNION\n"
    sql += separator.join(ex_tables_sql)
    sql += ") all_exceptions;"
    sql_file.writelines(sql)
    sql_file.close()


def pre_validation():
    if is_staging is False:
        log.info(f"Validating with SIRIUS")
        log.info(f"Copying casrec csv source data to Sirius for comparison work")
        copy_schema(
            log=log,
            sql_path=sql_path,
            from_config=config.db_config["migration"],
            from_schema=config.schemas["pre_transform"],
            to_config=config.db_config["target"],
            to_schema=config.schemas["pre_transform"],
        )
    else:
        log.info(f"Validating with STAGING schema")

    log.info(f"INSTALL TRANSFORMATION ROUTINES")
    execute_sql_file(
        sql_path, transformations_sqlfile, conn_target, config.schemas["public"]
    )

    log.info(f"GENERATE SQL")

    log.info("- Lookup Functions")
    build_lookup_functions()
    log.info("- Drop Exception Tables")
    drop_exception_tables()

    global mapping_dict

    for mapping_name in mappings_to_run:
        mapping_dict = helpers.get_mapping_dict(
            file_name=mapping_name + "_mapping", only_complete_fields=True, include_pk=False
        )
        log.info(mapping_name)

        log.info("- Exception Table")
        build_exception_table(mapping_name)

        log.info("- Table Validation Statement")
        build_validation_statements(mapping_name)

        log.info("- Column Validation Statements")
        build_column_validation_statements(mapping_name)
    #
    write_validation_sql()


def post_validation():
    log.info(f"REMOVE TRANSFORMATION ROUTINES")
    execute_sql_file(
        sql_path, f"drop_{transformations_sqlfile}", conn_target, config.schemas["public"]
    )

    log.info("REPORT")
    mapping_df = get_mapping_report_df()
    write_results_sql()
    exceptions_df = df_from_sql_file(sql_path_temp, results_sqlfile, conn_target)
    report_df = mapping_df.merge(exceptions_df, on="mapping")
    headers = [
        "Casrec Mapping",
        "Rows",
        "Unmapped",
        "Mapped",
        "Complete (%)",
        "Attempted",
        "Failed",
        "Fail rate",
        "Mismatches in...",
    ]
    print(tabulate(report_df, headers, tablefmt="psql"))


def set_validation_target():
    global conn_target, target_schema
    db_config = "migration" if is_staging else "target"
    conn_target = psycopg2.connect(config.get_db_connection_string(db_config))
    target_schema = "staging" if is_staging else "public"


def get_exception_count():
    write_get_exception_count_sql()
    return result_from_sql_file(sql_path_temp, total_exceptions_sqlfile, conn_target)


@click.command()
@click.option("-v", "--verbose", count=True)
@click.option("--staging", is_flag=True, default=False)
def main(verbose, staging):
    set_logging_level(verbose)
    log.info(helpers.log_title(message="Validation"))

    global is_staging
    is_staging = staging
    set_validation_target()

    pre_validation()

    log.info("RUN VALIDATION")
    execute_sql_file(
        sql_path_temp, validation_sqlfile, conn_target, config.schemas["public"]
    )

    post_validation()

    log.info("Adding sql files to bucket...\n")#
    s3 = get_s3_session(session, environment, host)
    if ci != "true":
        for file in os.listdir(sql_path_temp):
            file_path = f"{sql_path_temp}/{file}"
            s3_file_path = f"validation/sql/{file}"
            if file.endswith(".sql"):
                upload_file(bucket_name, file_path, s3, log, s3_file_path)

    if get_exception_count() > 0:
        exit(1)

    log.info("No exceptions found: continue...\n")


if __name__ == "__main__":
    t = time.process_time()

    log.setLevel(1)
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    validation_dict = get_validation_dict()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
