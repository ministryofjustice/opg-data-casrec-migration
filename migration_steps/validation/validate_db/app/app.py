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
mapping_path = current_path / "../../../shared/mapping_definitions"
shared_sql_path = current_path / "../../../shared/sql"
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

mappings_to_run = [
    "client_persons",
    # "client_addresses",
    # "client_phonenumbers",
    # "cases",
    # "person_caseitem"
]

indent = "    "
results_sqlfile = "get_validation_results.sql"
validation_sqlfile = "validation.sql"
total_exceptions_sqlfile = "get_exceptions_total.sql"
host = os.environ.get("DB_HOST")
ci = os.getenv("CI")
bucket_name = f"casrec-migration-{environment.lower()}"
account = os.environ["SIRIUS_ACCOUNT"]
session = boto3.session.Session()


def set_logging_level(verbose):
    try:
        log.setLevel(verbosity_levels[verbose])
    except KeyError:
        log.setLevel("INFO")
        log.info(f"{verbose} is not a valid verbosity level")


def get_mapping_report_df():
    file_path = mapping_path / "summary/mapping_progress_summary.json"
    summary_dict = json.load(open(file_path))

    mappings = []
    for worksheet, worksheet_summary in summary_dict["worksheets"].items():
        if worksheet in mappings_to_run:
            mappings.append([worksheet] + list(worksheet_summary.values()))

    return pd.DataFrame.from_records(
        mappings, columns=["mapping", "rows", "unmapped", "mapped", "complete"]
    )


def get_sirius_table(mapping):
    mapping_name_to_table = {
        "client_persons": "persons",
        "client_addresses": "addresses",
        "client_phonenumbers": "phonenumbers",
    }
    return mapping_name_to_table.get(mapping)


def get_casrec_from(mapping):
    mapping_name_to_table = {"client_persons": "pat"}
    return mapping_name_to_table.get(mapping)


def get_exception_table(mapping):
    return f"exceptions_{mapping}"


def build_exception_tables(sql_lines):
    # drop all possible exception tables from last run
    for mapfile in helpers.get_all_mapped_fields().keys():
        sql_lines.append(
            f"DROP TABLE IF EXISTS {source_schema}.{get_exception_table(mapfile)};\n"
        )
    sql_lines.append("\n\n")

    for mapping in mappings_to_run:
        exception_table_name = get_exception_table(mapping)
        map_dict = helpers.get_mapping_dict(
            file_name=mapping + "_mapping", only_complete_fields=True, include_pk=False
        )
        sql_lines.append(f"CREATE TABLE {source_schema}.{exception_table_name}(\n")
        separator = ",\n"
        cols = separator.join(
            [
                f"{indent}{sirius_col} text default NULL"
                for sirius_col in map_dict.keys()
            ]
        )
        sql_lines.append(cols)
        sql_lines.append("\n);\n\n")


def build_lookup_functions(sql_lines):
    # drop all the lookup tables from last run
    for lookup_name, lookup in helpers.get_all_lookup_dicts().items():
        sql_lines.append(
            f"DROP FUNCTION IF EXISTS {source_schema}.{lookup_name}(character varying);\n"
        )
    sql_lines.append("\n\n")

    for lookup_name, lookup in helpers.get_all_lookup_dicts().items():
        sql_lines.append(
            f"CREATE OR REPLACE FUNCTION {source_schema}.{lookup_name}(lookup_key varchar default null) RETURNS TEXT AS\n"
        )
        sql_lines.append(f"$$\n")
        sql_lines.append(f"{indent}SELECT CASE\n")
        for k, v in lookup.items():
            try:
                sirius_value = v["sirius_mapping"].replace("'", "''")
            except AttributeError:
                sirius_value = v["sirius_mapping"]
            sql_lines.append(
                f"{indent}{indent}WHEN ($1 = '{k}') THEN '{sirius_value}'\n"
            )
        sql_lines.append(f"{indent}END\n")
        sql_lines.append("$$ LANGUAGE sql;\n\n\n")


def format_calculated_value(mapping):
    callables = {
        "current_date": "'"
        + datetime.now().strftime("%Y-%m-%d")
        + "'"  # just do today's date
    }
    return callables.get(mapping["transform_casrec"]["calculated"])


def format_default_value(mapping):
    default_value = mapping["transform_casrec"]["default_value"]
    if mapping["sirius_details"]["data_type"] in ["date", "datetime", "str"]:
        default_value = f"'{default_value}'"
    return default_value


def get_sirius_from(mapping):
    return f"{target_schema}." + mapping["sirius_details"]["table_name"]


def wrap_sirius_datatype_functions(mapping, col_name):
    sql = col_name
    if "current_date" == mapping["transform_casrec"]["calculated"]:
        sql = f"CAST({col_name} AS DATE)"
    return sql


def get_sirius_col_name(mapping, col_name):
    col_table = mapping["sirius_details"]["table_name"]
    return f"{col_table}.{col_name}"


def build_sirius_cols(map_dict):
    sirius_cols = []
    for k, v in map_dict.items():
        sirius_cols.append(
            f"{indent}{indent}{indent}{wrap_sirius_datatype_functions(v, get_sirius_col_name(v, k))} AS {k}"
        )

    separator = ",\n"
    return separator.join(sirius_cols)


def wrap_casrec_col_conversion_functions(mapping, col):
    datatype = mapping["sirius_details"]["data_type"]
    if datatype in ["date"]:
        wrapped_col = f"CAST(NULLIF(NULLIF(TRIM({col}), 'NaT'), '') AS DATE)"
    elif datatype in ["datetime"]:
        if "current_date" == mapping["transform_casrec"]["calculated"]:
            wrapped_col = f"CAST(NULLIF(TRIM({col}), '') AS DATE)"
        else:
            wrapped_col = (
                f"CAST(NULLIF(NULLIF(TRIM({col}), 'NaT'), '') AS TIMESTAMP(0))"
            )
    elif datatype in ["bool", "int"]:
        wrapped_col = col
    else:
        wrapped_col = f"NULLIF(TRIM({col}), '')"

    return wrapped_col


def get_casrec_col_value(mapping):
    casrec_col_table = None
    if mapping["transform_casrec"]["casrec_table"]:
        casrec_col_table = mapping["transform_casrec"]["casrec_table"].lower()
        col = get_full_casrec_column_name(mapping)
        if "" != mapping["transform_casrec"]["lookup_table"]:
            db_lookup_func = mapping["transform_casrec"]["lookup_table"]
            col = f"{source_schema}.{db_lookup_func}({col})"
    elif "" != mapping["transform_casrec"]["default_value"]:
        col = format_default_value(mapping)
    elif "" != mapping["transform_casrec"]["calculated"]:
        col = format_calculated_value(mapping)

    return casrec_col_table, col


def build_casrec_cols(map_dict):
    casrec_cols = []
    casrec_tables = []
    for k, v in map_dict.items():
        col_table, col_value = get_casrec_col_value(v)
        casrec_tables.append(f"{source_schema}.{col_table}")
        casrec_cols.append(
            f"{indent}{indent}{indent}{wrap_casrec_col_conversion_functions(v, col_value)} AS {k}"
        )
    separator = ",\n"
    casrec_cols = separator.join(casrec_cols)
    separator = ","
    casrec_tables = separator.join(set(casrec_tables))
    casrec_tables = separator.join(set(casrec_tables))
    return casrec_cols, casrec_tables


def get_full_casrec_column_name(mapping):
    casrec_col_table = mapping["transform_casrec"]["casrec_table"].lower()
    casrec_col_name = mapping["transform_casrec"]["casrec_column_name"]
    return f'{casrec_col_table}."{casrec_col_name}"'


def build_validation_statements(sql_lines):
    for mapping in mappings_to_run:
        exception_table_name = get_exception_table(mapping)
        sirius_table_name = get_sirius_table(mapping)
        map_dict = helpers.get_mapping_dict(
            file_name=mapping + "_mapping", only_complete_fields=True, include_pk=False
        )

        casrec_cols, casrec_tables = build_casrec_cols(map_dict)
        sirius_cols = build_sirius_cols(map_dict)

        sql_lines.append(f"INSERT INTO {source_schema}.{exception_table_name}(\n")
        # casrec half
        sql_lines.append(f"{indent}SELECT * FROM(\n")
        sql_lines.append(f"{indent}{indent}SELECT DISTINCT\n")
        sql_lines.append(f"{casrec_cols}\n")
        sql_lines.append(
            f"{indent}{indent}FROM {source_schema}.{get_casrec_from(mapping)}\n"
        )
        sql_lines.append(f"{indent}{indent}ORDER BY caserecnumber ASC\n")
        sql_lines.append(f"{indent}) as csv_data\n")
        sql_lines.append(f"{indent}EXCEPT\n")
        # sirius half
        sql_lines.append(f"{indent}SELECT * FROM(\n")
        sql_lines.append(f"{indent}{indent}SELECT DISTINCT\n")
        sql_lines.append(sirius_cols + "\n")
        sql_lines.append(f"{indent}{indent}FROM {target_schema}.{sirius_table_name}\n")
        sql_lines.append(f"{indent}{indent}WHERE clientsource = 'CASRECMIGRATION'\n")
        sql_lines.append(f"{indent}{indent}ORDER BY caserecnumber ASC\n")
        sql_lines.append(f"{indent}) as sirius_data\n")
        sql_lines.append(");\n\n")


def build_column_validation_statements(sql_lines):
    for mapping in mappings_to_run:
        map_dict = helpers.get_mapping_dict(
            file_name=mapping + "_mapping", only_complete_fields=True, include_pk=False
        )

        exception_table = f"{source_schema}.{get_exception_table(mapping)}"

        sql_lines.append(
            f"ALTER TABLE {exception_table} DROP COLUMN IF EXISTS vary_columns;\n"
        )
        sql_lines.append(
            f"ALTER TABLE {exception_table} ADD vary_columns varchar(255)[];\n\n"
        )

        if "caserecnumber" in map_dict:
            del map_dict["caserecnumber"]

        for k, v in map_dict.items():
            col_table, col_value = get_casrec_col_value(v)

            sql_lines.append(f"-- {k}\n")
            sql_lines.append(f"UPDATE {exception_table}\n")
            sql_lines.append(f"SET vary_columns = array_append(vary_columns, '{k}')\n")
            sql_lines.append(f"WHERE caserecnumber IN (\n")
            sql_lines.append(f"{indent}SELECT caserecnumber FROM (\n")

            # casrec half
            sql_lines.append(f"{indent}{indent}SELECT * FROM(\n")
            sql_lines.append(f"{indent}{indent}{indent}SELECT \n")
            sql_lines.append(
                f"{indent}{indent}{indent}{indent}exc_table.caserecnumber,\n"
            )
            sql_lines.append(
                f"{indent}{indent}{indent}{indent}{wrap_casrec_col_conversion_functions(v, col_value)} AS {k}\n"
            )
            sql_lines.append(f"{indent}{indent}{indent}FROM {source_schema}.pat\n")
            sql_lines.append(
                f"{indent}{indent}{indent}LEFT JOIN {exception_table} exc_table\n"
            )
            sql_lines.append(
                f'{indent}{indent}{indent}{indent}ON exc_table.caserecnumber = pat."Case"\n'
            )
            sql_lines.append(
                f"{indent}{indent}{indent}WHERE exc_table.caserecnumber IS NOT NULL\n"
            )
            sql_lines.append(
                f"{indent}{indent}{indent}ORDER BY exc_table.caserecnumber\n"
            )
            sql_lines.append(f"{indent}{indent}) as csv_data\n")

            sql_lines.append(f"{indent}{indent}EXCEPT\n")

            # sirius half
            sql_lines.append(f"{indent}{indent}SELECT * FROM(\n")
            sql_lines.append(f"{indent}{indent}{indent}SELECT\n")
            sql_lines.append(
                f"{indent}{indent}{indent}{indent}exc_table.caserecnumber,\n"
            )
            sql_lines.append(
                f"{indent}{indent}{indent}{indent}{get_sirius_col_name(v, k)} AS {k}\n"
            )
            sql_lines.append(f"{indent}{indent}{indent}FROM {get_sirius_from(v)}\n")
            sql_lines.append(
                f"{indent}{indent}{indent}LEFT JOIN {exception_table} exc_table\n"
            )
            sql_lines.append(
                f"{indent}{indent}{indent}{indent}ON exc_table.caserecnumber = persons.caserecnumber\n"
            )
            sql_lines.append(
                f"{indent}{indent}{indent}WHERE exc_table.caserecnumber IS NOT NULL\n"
            )
            sql_lines.append(
                f"{indent}{indent}{indent}ORDER BY exc_table.caserecnumber\n"
            )
            sql_lines.append(f"{indent}{indent}) as sirius_data\n")

            sql_lines.append(f"{indent}) as vary\n")
            sql_lines.append(");\n\n")


def write_validation_sql(sql_lines):
    log.debug(f"Writing to file")
    validation_sql_path = shared_sql_path / validation_sqlfile
    validation_sql_file = open(validation_sql_path, "w")
    validation_sql_file.writelines(sql_lines)
    validation_sql_file.close()
    log.debug(f"Saved to file: {validation_sql_path}")


def write_results_sql():
    sql_file = open(shared_sql_path / results_sqlfile, "w")
    results_rows = []
    for mapping in mappings_to_run:
        exception_table_name = get_exception_table(mapping)
        casrec_table_name = get_casrec_from(mapping)
        results_rows.append(
            f"SELECT '{mapping}' AS mapping,"
            f"(SELECT COUNT(*) FROM {source_schema}.{casrec_table_name}) as attempted,"
            f"(SELECT COUNT(*) FROM {source_schema}.{exception_table_name}),"
            f"(SELECT CONCAT( CAST( CAST( "
            f"(SELECT COUNT(*) FROM {source_schema}.{exception_table_name}) / "
            f"(SELECT COUNT(*) FROM {source_schema}.{casrec_table_name})::FLOAT AS numeric ) AS TEXT), '%')),"
            f"(SELECT json_agg(vary) AS affected_columns FROM ("
            f"SELECT DISTINCT unnest(vary_columns) as vary FROM {source_schema}.{exception_table_name}"
            f") t1)\n"
        )
    separator = "UNION\n"
    sql_file.writelines(separator.join(results_rows))
    sql_file.close()


def write_get_exception_count_sql():
    sql_file = open(shared_sql_path / total_exceptions_sqlfile, "w")
    sql_lines = f"SELECT SUM(exceptions) FROM (\n"

    ex_tables_sql = []
    for mapping in mappings_to_run:
        exception_table_name = get_exception_table(mapping)
        ex_tables_sql.append(
            f"{indent}SELECT COUNT(*) as exceptions, 'client_persons' "
            f"FROM {source_schema}.{exception_table_name}\n"
        )

    separator = f"{indent}UNION\n"
    sql_lines += separator.join(ex_tables_sql)
    sql_lines += ") all_exceptions;"
    sql_file.writelines(sql_lines)
    sql_file.close()


def pre_validation():
    if is_staging is False:
        log.info(f"Validating with SIRIUS")
        log.info(f"Copying casrec csv source data to Sirius for comparison work")
        copy_schema(
            log=log,
            sql_path=shared_sql_path,
            from_config=config.db_config["migration"],
            from_schema=config.schemas["pre_transform"],
            to_config=config.db_config["target"],
            to_schema=config.schemas["pre_transform"],
        )
    else:
        log.info(f"Validating with STAGING schema")

    log.info(f"GENERATE SQL")
    sql_lines = []

    log.info("- Exception Tables")
    build_exception_tables(sql_lines)

    log.info("- Lookup Functions")
    build_lookup_functions(sql_lines)

    log.info("- Validation SQL")
    build_validation_statements(sql_lines)

    log.info("- Column insight")
    build_column_validation_statements(sql_lines)

    log.info(f"Printing Lines:")

    write_validation_sql(sql_lines)


def post_validation():
    log.info("REPORT")
    mapping_df = get_mapping_report_df()
    write_results_sql()
    exceptions_df = df_from_sql_file(shared_sql_path, results_sqlfile, conn_target)
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
    return result_from_sql_file(shared_sql_path, total_exceptions_sqlfile, conn_target)


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
        shared_sql_path, validation_sqlfile, conn_target, config.schemas["public"]
    )
    log.info("- ok\n")

    post_validation()

    if get_exception_count() > 0:
        exit(1)

    log.info("No exceptions found: continue...\n")
    log.info("Adding sql files to bucket...\n")

    s3 = get_s3_session(session, environment, host)
    if ci != "true":
        for file in os.listdir(shared_sql_path):
            file_path = f"{shared_sql_path}/{file}"
            s3_file_path = f"validation/sql/{file}"
            if file.endswith(".sql"):
                upload_file(bucket_name, file_path, s3, log, s3_file_path)


if __name__ == "__main__":
    t = time.process_time()

    log.setLevel(1)
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
