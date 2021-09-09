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
fixed_entity_sql_dir = current_path / "fixed_sql"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
config = get_config(environment)

# logging
log = logging.getLogger("root")
custom_logger.setup_logging(env=environment, module_name="validate db")
is_staging = False
conn_target = None
target_schema = None
source_schema = config.schemas["pre_transform"]
mapping_dict = None
validation_dict = None


def get_mappings():
    mappings_to_run = []

    allowed_entities = config.allowed_entities(env=os.environ.get("ENVIRONMENT"))
    all_mappings = {
        "clients": [
            "client_addresses",
            "client_persons",
            "client_phonenumbers",
            "client_death_notifications",
        ],
        "cases": ["cases"],
        # "bonds": ["bonds"],
        "crec": [
            "crec_persons",
        ],
        "supervision_level": [
            "supervision_level_log",
        ],
        "deputies": [
            "deputy_persons",
            "deputy_death_notifications",
        ],
        "warnings": [
            "client_nodebtchase_warnings",
            "client_saarcheck_warnings",
            "client_special_warnings",
            "client_violent_warnings",
            "deputy_special_warnings",
            "deputy_violent_warnings",
        ],
        # "visits": ["visits"],
        # "remarks": ["notes"]
    }

    for entity, mapping in all_mappings.items():
        if entity in allowed_entities:
            mappings_to_run = mappings_to_run + mapping

    return mappings_to_run


mappings_to_run = get_mappings()
results_sqlfile = "get_validation_results.sql"
validation_sqlfile = "validation.sql"
transformations_sqlfile = "transformation_functions.sql"
total_exceptions_sqlfile = "get_exceptions_total.sql"
host = os.environ.get("DB_HOST")
ci = os.getenv("CI")
account_name = os.environ.get("ACCOUNT_NAME")
bucket_name = f"casrec-migration-{account_name.lower()}"
account = os.environ["SIRIUS_ACCOUNT"]
session = boto3.session.Session()
sql_lines = []
sql_statement_lines = []
statement_count = 0


def get_validation_dict(mapping_name):
    file_path = shared_path / "validation_mapping.json"
    validation_dict = json.load(open(file_path))
    return validation_dict[mapping_name]


def get_mapping_report_df():
    file_path = (
        shared_path / "mapping_definitions/summary/mapping_progress_summary.json"
    )
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
        sql_add(f"DROP TABLE IF EXISTS {get_exception_table(mapfile)};")
    sql_add("")


def build_exception_table(mapping_name):
    exclude_cols = validation_dict["exclude"] + list(validation_dict["orderby"].keys())

    sql_add(f"-- {mapping_name}")
    sql_add(f"CREATE TABLE {get_exception_table(mapping_name)}(")

    sql_add(f"caserecnumber text default NULL,", 1)

    # for SELECT DISTINCT, ORDER BY expressions must appear in select list
    for col in list(validation_dict["orderby"].keys()):
        sql_add(f"{col} text default NULL,", 1)

    # other columns
    separator = ",\n"
    sql_add(
        separator.join(
            [
                f"    {col} text default NULL"
                for col in mapping_dict.keys()
                if col not in exclude_cols
            ]
        )
    )
    sql_add(");", 0, 2)


def build_lookup_functions():
    for lookup_name, lookup in helpers.get_all_lookup_dicts().items():

        firstval = lookup[list(lookup)[0]]["sirius_mapping"]
        datatype = "TEXT"
        if isinstance(firstval, bool):
            datatype = "BOOLEAN"
        elif isinstance(firstval, int):
            datatype = "INT"

        sql_add(
            f"DROP FUNCTION IF EXISTS {source_schema}.{lookup_name}(character varying);"
        )
        sql_add(
            f"CREATE OR REPLACE FUNCTION {source_schema}.{lookup_name}(lookup_key varchar default null) RETURNS {datatype} AS"
        )
        sql_add(f"$$")
        sql_add(f"SELECT CASE", 1)
        for k, v in lookup.items():
            try:
                escape_quotes = v["sirius_mapping"].replace("'", "''")
            except AttributeError:
                escape_quotes = v["sirius_mapping"]

            value = (
                f"'{escape_quotes}'"
                if isinstance(escape_quotes, str)
                else escape_quotes
            )
            sql_add(f"WHEN ($1 = '{k}') THEN {value}", 2)

        sql_add("END", 1)
        sql_add("$$ LANGUAGE sql;", 0, 2)
    sql_add("")


def wrap_override_sql(col_name: str, side, sql):
    transform_cols = validation_dict[side]["transform"]
    if col_name in transform_cols.keys():
        sql = validation_dict[side]["transform"][col_name].replace("{col}", str(sql))
    return sql


def wrap_sirius_col(col_name: str, col_definition, sql: str):
    # first wrap override, if any
    sql = wrap_override_sql(col_name, "sirius", sql)

    # convert empty strings to NULL
    if (
        "str" == col_definition["sirius_details"]["data_type"]
        and col_name != "caserecnumber"
    ):
        sql = f"NULLIF(TRIM({sql}), '')"
    return sql


def wrap_casrec_col(col_name: str, col_definition, sql: str):
    # first wrap override, if any
    sql = wrap_override_sql(col_name, "casrec", sql)

    # convert empty strings to NULL
    if (
        col_definition["sirius_details"]["data_type"] not in ["bool", "int"]
        and col_name != "caserecnumber"
    ):
        sql = f"NULLIF(TRIM({sql}), '')"

    # wrap transform, if required
    if col_definition["transform_casrec"]["requires_transformation"]:
        transform_func = col_definition["transform_casrec"]["requires_transformation"]
        sql = f"transf_{transform_func}({sql})"

    # calculated = col_definition["transform_casrec"]["calculated"]
    # cast to datatype - why are we casting casrec side to anything at all??
    # if datatype in ["date"]:
    #     col = f"CAST(NULLIF(NULLIF(TRIM({col}), 'NaT'), '') AS DATE)"
    # elif datatype in ["datetime"]:
    #     if "current_date" == calculated:
    #         col = f"CAST(NULLIF(TRIM({col}), '') AS DATE)"
    #     else:
    #         col = f"CAST(NULLIF(NULLIF(TRIM({col}), 'NaT'), '') AS TIMESTAMP(0))"
    # elif datatype in ["int"]:
    #     col = f"CAST({col} AS INT)"

    return sql


def get_casrec_default_value(mapped_col_key: str):
    default_value = mapping_dict[mapped_col_key]["transform_casrec"]["default_value"]
    data_type = mapping_dict[mapped_col_key]["sirius_details"]["data_type"]

    if data_type in ["date", "datetime", "str"]:
        default_value = f"'{default_value}'"
    elif data_type == "bool":
        default_value = default_value in ["true", "True", 1]

    return default_value


def get_casrec_calculated_value(col_key: str):
    callables = {
        "current_date": "'"
        + datetime.now().strftime("%Y-%m-%d")
        + "'"  # just do today's date
    }
    return callables.get(mapping_dict[col_key]["transform_casrec"]["calculated"])


def get_col_definition(col_key: str):
    col_key_parts = col_key.split(".")
    if len(col_key_parts) == 1:
        # 'local' definition from same json
        col_definition = mapping_dict[col_key_parts[0]]
    else:
        # definition exists in other json
        col_mapping = helpers.get_mapping_dict(
            file_name=col_key_parts[0] + "_mapping",
            only_complete_fields=True,
            include_pk=False,
        )
        col_definition = col_mapping[col_key_parts[1]]
    return col_definition


def get_sirius_col_source(col_name: str, col_definition):
    table = col_definition["sirius_details"]["table_name"]
    sql = f"{table}.{col_name}"
    return sql


def get_casrec_col_source(col_key: str, col_definition):
    sql = ""
    col_definition = col_definition["transform_casrec"]
    if col_definition["casrec_table"]:
        table = col_definition["casrec_table"].lower()
        col_name = col_definition["casrec_column_name"]
        sql = f'{source_schema}.{table}."{col_name}"'
        if "" != col_definition["lookup_table"]:
            db_lookup_func = col_definition["lookup_table"]
            sql = f"{source_schema}.{db_lookup_func}({sql})"
    elif "" != col_definition["default_value"]:
        sql = get_casrec_default_value(col_key)
    elif "" != col_definition["calculated"]:
        sql = get_casrec_calculated_value(col_key)
    return sql


def get_col_name_from_key(col_key: str):
    col_key_parts = col_key.split(".")
    if len(col_key_parts) == 1:
        col_name = col_key_parts[0]
    else:
        col_name = col_key_parts[1]
    return col_name


def casrec_wrap(col_key: str):
    col_name = get_col_name_from_key(col_key)
    col_definition = get_col_definition(col_key)
    sql = get_casrec_col_source(col_key, col_definition)
    sql = wrap_casrec_col(col_name, col_definition, sql)
    return sql


def sirius_wrap(col_key: str):
    col_name = get_col_name_from_key(col_key)
    col_definition = get_col_definition(col_key)
    sql = get_sirius_col_source(col_name, col_definition)
    sql = wrap_sirius_col(col_name, col_definition, sql)
    return sql


def build_validation_statements(mapping_name):
    exclude_cols = validation_dict["exclude"] + list(validation_dict["orderby"].keys())
    order_by = ",\n        ".join(
        ["caserecnumber ASC"] + list(validation_dict["orderby"].keys())
    )
    col_separator = ",\n"

    sql_add(f"INSERT INTO {get_exception_table(mapping_name)}(")

    # CASREC half
    sql_add("SELECT * FROM(", 1)
    sql_add("SELECT DISTINCT", 2)

    sql_add(f'{casrec_wrap(validation_dict["casenumber_source"])} AS caserecnumber,', 3)

    # for SELECT DISTINCT, ORDER BY expressions must appear in select list
    for order_mapped_item_name, mapped_item_key in validation_dict["orderby"].items():
        sql_add(
            f"{casrec_wrap(mapped_item_key['mapping_table'])} AS {order_mapped_item_name},",
            3,
        )

    # standard cols
    sql_add(
        col_separator.join(
            [
                f"            {casrec_wrap(mapped_item)} AS {mapped_item}"
                for mapped_item in mapping_dict.keys()
                if mapped_item not in exclude_cols
            ]
        )
    )

    # FROM, with JOINs
    sql_add(
        f"FROM {source_schema}.{validation_dict['casrec']['from_table']}",
        2,
    )
    for join in validation_dict["casrec"]["joins"]:
        sql_add(f"{join}", 2)

    # WHERE
    sql_add("WHERE True", 2)
    for where_clause in validation_dict["casrec"]["where_clauses"]:
        sql_add(f"AND {where_clause}", 2)

    # ORDER
    sql_add(f"ORDER BY {order_by}", 2)
    sql_add(") as csv_data", 1)
    sql_add("EXCEPT", 1)

    # SIRIUS half
    sql_add("SELECT * FROM(", 1)
    sql_add("SELECT DISTINCT", 2)

    sql_add(f'{sirius_wrap(validation_dict["casenumber_source"])} AS caserecnumber,', 3)

    # for SELECT DISTINCT, ORDER BY expressions must appear in select list
    for order_mapped_item_name, mapped_item_key in validation_dict["orderby"].items():
        sql_add(
            f"{sirius_wrap(mapped_item_key['mapping_table'])} AS {order_mapped_item_name},",
            3,
        )

    # standard cols
    sql_add(
        col_separator.join(
            [
                f"            {sirius_wrap(mapped_item)} AS {mapped_item}"
                for mapped_item in mapping_dict.keys()
                if mapped_item not in exclude_cols
            ]
        )
    )

    # FROM, with JOINs
    sql_add(
        f"FROM {target_schema}.{validation_dict['sirius']['from_table']}",
        2,
    )
    for join in validation_dict["sirius"]["joins"]:
        join = join.replace("{target_schema}", str(target_schema))
        sql_add(f"{join}", 2)

    # WHERE
    sql_add("WHERE True", 2)
    for where_clause in validation_dict["sirius"]["where_clauses"]:
        sql_add(f"AND {where_clause}", 2)

    # ORDER
    sql_add(f"ORDER BY {order_by}", 2)
    sql_add(") as sirius_data", 1)
    sql_add(");", 0, 2)


def sql_add(sql, indent_level=0, line_breaks=1):
    global sql_lines
    global sql_statement_lines
    indent = "    " * indent_level
    breaks = "\n" * line_breaks
    sql_lines.append(f"{indent}{sql}{breaks}")
    sql_statement_lines.append(f"{indent}{sql}{breaks}")


def write_column_validation_sql(
    mapping_name, mapped_item_name, col_source_casrec, col_source_sirius
):
    order_by = ",\n        ".join(
        ["exc_caserecnumber ASC"] + list(validation_dict["orderby"].keys())
    )

    sql_add(f"-- {mapping_name} / {mapped_item_name}")
    sql_add(f"UPDATE {get_exception_table(mapping_name)}")
    sql_add(f"SET vary_columns = array_append(vary_columns, '{mapped_item_name}')")
    sql_add("WHERE caserecnumber IN (")
    sql_add(f"SELECT exc_caserecnumber FROM (", 1)

    # casrec half
    sql_add("SELECT * FROM(", 2)
    sql_add("SELECT", 3)
    # caserecnumber
    sql_add("exc_table.caserecnumber AS exc_caserecnumber,", 4)

    # for SELECT DISTINCT, ORDER BY expressions must appear in select list
    for order_mapped_item_name, order_mapped_item in validation_dict["orderby"].items():
        sql_add(
            f"{casrec_wrap(order_mapped_item['mapping_table'])} AS {order_mapped_item_name},",
            4,
        )
    # tested column
    sql_add(f"{col_source_casrec} AS {mapped_item_name}", 4)
    sql_add(
        f"FROM {source_schema}.{validation_dict['casrec']['from_table']}",
        3,
    )
    for join in validation_dict["casrec"]["joins"]:
        sql_add(f"{join}", 3)
    exception_table_join = validation_dict["casrec"]["exception_table_join"]
    sql_add(f"{exception_table_join}", 3)
    # WHERE
    sql_add("WHERE exc_table.caserecnumber IS NOT NULL", 3)
    for where_clause in validation_dict["casrec"]["where_clauses"]:
        sql_add(f"AND {where_clause}", 4)

    sql_add(f"ORDER BY {order_by}", 3)
    sql_add(") as csv_data", 2)

    sql_add("EXCEPT", 2)

    # sirius half
    sql_add("SELECT * FROM(", 2)
    sql_add("SELECT", 3)
    # caserecnumber
    sql_add("exc_table.caserecnumber AS exc_caserecnumber,", 4)

    # for SELECT DISTINCT, ORDER BY expressions must appear in select list
    for order_mapped_item_name, order_mapped_item in validation_dict["orderby"].items():
        sql_add(
            f"{sirius_wrap(order_mapped_item['mapping_table'])} AS {order_mapped_item_name},",
            4,
        )

    # tested column
    sql_add(f"{col_source_sirius} AS {mapped_item_name}", 4)
    sql_add(
        f"FROM {target_schema}.{validation_dict['sirius']['from_table']}",
        3,
    )
    for join in validation_dict["sirius"]["joins"]:
        join = join.replace("{target_schema}", str(target_schema))
        sql_add(f"{join}", 3)
    exception_table_join = validation_dict["sirius"]["exception_table_join"]
    sql_add(f"{exception_table_join}", 3)
    # WHERE
    sql_add("WHERE exc_table.caserecnumber IS NOT NULL", 3)
    for where_clause in validation_dict["sirius"]["where_clauses"]:
        sql_add(f"AND {where_clause}", 4)
    sql_add(f"ORDER BY {order_by}", 3)
    sql_add(") as sirius_data", 2)

    sql_add(") as vary", 1)
    sql_add(");", 0, 2)


def build_column_validation_statements(mapping_name):
    sql_add(
        f"ALTER TABLE {get_exception_table(mapping_name)} DROP COLUMN IF EXISTS vary_columns;"
    )
    sql_add(
        f"ALTER TABLE {get_exception_table(mapping_name)} ADD vary_columns varchar(255)[];",
        0,
        2,
    )
    output_statement_to_file()

    # test regular columns
    for mapped_item_name in mapping_dict.keys():
        if mapped_item_name not in validation_dict["exclude"]:
            write_column_validation_sql(
                mapping_name,
                mapped_item_name,
                casrec_wrap(mapped_item_name),
                sirius_wrap(mapped_item_name),
            )
            output_statement_to_file()


def write_validation_sql():
    global sql_lines
    log.debug(f"Writing to file")
    validation_sql_path = sql_path_temp / validation_sqlfile
    validation_sql_file = open(validation_sql_path, "w")
    validation_sql_file.writelines(sql_lines)
    validation_sql_file.close()
    log.debug(f"Saved to file: {validation_sql_path}")


def write_results_sql():
    global validation_dict
    sql_file = open(sql_path_temp / results_sqlfile, "w")
    print(sql_path_temp / results_sqlfile)
    results_rows = []
    for mapping_name in mappings_to_run:
        validation_dict = get_validation_dict(mapping_name)
        casrec_table_name = validation_dict["casrec"]["from_table"]
        results_rows.append(
            f"SELECT '{mapping_name}' AS mapping,\n"
            f"(SELECT COUNT(*) FROM {source_schema}.{casrec_table_name}) as attempted,\n"
            f"(SELECT COUNT(*) FROM {get_exception_table(mapping_name)}),\n"
            f"(SELECT CONCAT( CAST( CAST( (\n"
            f"    (SELECT COUNT(*) FROM {get_exception_table(mapping_name)}) / \n"
            f"    (SELECT COUNT(*) FROM {source_schema}.{casrec_table_name})::FLOAT) * 100 AS NUMERIC) AS TEXT), '%'))\n"
            # f"CAST((SELECT json_agg(vary) AS affected_columns FROM (\n"
            # f"    SELECT DISTINCT unnest(vary_columns) as vary FROM {get_exception_table(mapping_name)}\n"
            # f") t1) AS TEXT)\n"
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


def output_statement_to_file():
    global statement_count
    global sql_statement_lines
    statement_count += 1
    statement_file_name = (
        f"{sql_path_temp}/validation_statement_{str(statement_count).zfill(3)}.sql"
    )
    validation_sql_file = open(statement_file_name, "w")
    validation_sql_file.writelines(sql_statement_lines)
    validation_sql_file.close()
    log.debug(f"Saved to file: {statement_file_name}")
    sql_statement_lines = []


def clear_local_temp_sql():
    if os.path.exists(sql_path_temp):
        for file in os.listdir(sql_path_temp):
            file_path = f"{sql_path_temp}/{file}"
            if "validation.sql" or "validation_statement" in file:
                os.remove(file_path)
    else:
        os.mkdir(sql_path_temp)


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

    clear_local_temp_sql()

    log.info(f"INSTALL TRANSFORMATION ROUTINES")
    execute_sql_file(
        sql_path, transformations_sqlfile, conn_target, config.schemas["public"]
    )

    log.info(f"GENERATE SQL")

    log.info("Lookup Functions")
    build_lookup_functions()
    output_statement_to_file()

    log.info("Drop Exception Tables")
    drop_exception_tables()
    output_statement_to_file()

    global mapping_dict, validation_dict

    for mapping_name in mappings_to_run:
        log.info(f"Entity: {mapping_name}")

        mapping_dict = helpers.get_mapping_dict(
            file_name=mapping_name + "_mapping",
            only_complete_fields=True,
            include_pk=False,
        )

        validation_dict = get_validation_dict(mapping_name)

        fixed_sql_path = f"{fixed_entity_sql_dir}/{mapping_name}.sql"
        if os.path.exists(fixed_sql_path):
            log.debug(f"Static validation file found! {fixed_sql_path}")
            fixedfile = open(fixed_sql_path, "r")
            for line in fixedfile:
                sql_add(line.replace("{target_schema}", str(target_schema)))
            output_statement_to_file()
        else:
            log.debug("Exception Table")
            build_exception_table(mapping_name)
            output_statement_to_file()

            log.debug("Table Validation Statement")
            build_validation_statements(mapping_name)
            output_statement_to_file()

            # log.debug("Column Validation Statements")
            # build_column_validation_statements(mapping_name)

    write_validation_sql()


def post_validation():
    log.info(f"REMOVE TRANSFORMATION ROUTINES")
    execute_sql_file(
        sql_path,
        f"drop_{transformations_sqlfile}",
        conn_target,
        config.schemas["public"],
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
        # "Mismatches in...",
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
@click.option("--staging", is_flag=True, default=False)
def main(staging):

    log.info(helpers.log_title(message="Validation"))

    global is_staging
    is_staging = staging
    set_validation_target()

    pre_validation()

    log.info("Adding sql files to bucket...\n")  #
    s3 = get_s3_session(session, environment, host)
    if ci != "true":
        for file in os.listdir(sql_path_temp):
            file_path = f"{sql_path_temp}/{file}"
            s3_file_path = f"validation/sql/{file}"
            if file.endswith(".sql"):
                upload_file(bucket_name, file_path, s3, log, s3_file_path)

    log.info("RUN VALIDATION")

    for file in sorted(os.listdir(sql_path_temp)):
        if file.startswith("validation_statement_"):
            log.debug(f" Running {file}")
            execute_sql_file(sql_path_temp, file, conn_target, config.schemas["public"])

    log.info("RUN POST VALIDATION")
    post_validation()

    if get_exception_count() > 0:
        log.info("Exceptions WERE found: override / continue anyway\n")
        # exit(1)
    else:
        log.info("No exceptions found: continue...\n")


if __name__ == "__main__":
    t = time.process_time()

    log.setLevel(1)
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
