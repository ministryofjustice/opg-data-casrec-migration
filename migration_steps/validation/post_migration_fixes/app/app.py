"""
Usage:

python3 app.py
- run all post-migration scripts

python3 app.py some.sql
- run a single SQL script (in the post-migration tagged format)

python3 app.py some.sql dumpsql
- generate the SQL that would have been run for a single SQL script
(but don't run it); note that this will still create the casrec
mapping tables
"""
import os
import io
import re
from glob import glob
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import time
import sqlalchemy
import psycopg2
from helpers import get_config, log_title
from db_helpers import *
import logging
import custom_logger

environment = os.environ.get("ENVIRONMENT")
config = get_config(environment)

# logging
log = logging.getLogger("root")
log.addHandler(custom_logger.MyHandler())
config.custom_log_level()
verbosity_levels = config.verbosity_levels

source_db_conn_string = config.get_db_connection_string("migration")
source_engine = sqlalchemy.create_engine(source_db_conn_string)

target_db_conn_string = config.get_db_connection_string("target")
target_engine = sqlalchemy.create_engine(target_db_conn_string)

casrec_mapping_schema = f'casrec_mapping{config.migration_phase["suffix"]}'


def set_logging_level(verbose):
    try:
        log.setLevel(verbosity_levels[verbose])
    except KeyError:
        log.setLevel("INFO")
        log.info(f"{verbose} is not a valid verbosity level")


def _copy(create_sql, from_sql, to_table):
    # Export the data from casrec table(s)
    datafile = io.StringIO()

    casrec_raw_conn = source_engine.raw_connection()
    with casrec_raw_conn.cursor() as cur:
        cur.copy_expert(
            f"COPY ({sqlalchemy.text(from_sql)}) TO STDOUT WITH CSV HEADER", datafile
        )

    datafile.seek(0)

    # Set up destination table
    with target_engine.connect() as conn:
        conn.execute(sqlalchemy.text(create_sql))
        conn.execute(f"TRUNCATE {to_table}")

    # Import data into casrec_mapping table
    raw_conn = target_engine.raw_connection()
    with raw_conn.cursor() as cur:
        cur.copy_expert(f"COPY {to_table} FROM STDIN CSV HEADER", datafile)
    raw_conn.commit()


def copy_mapping_tables(casrec_mapping_schema):
    """
    Mapping tables.
    """
    with target_engine.begin() as conn:
        conn.execute(f"DROP SCHEMA IF EXISTS {casrec_mapping_schema} CASCADE;")
        conn.execute(f"CREATE SCHEMA IF NOT EXISTS {casrec_mapping_schema};")

    # Mapping from Sirius case ID to casrec Order No
    _copy(
        create_sql=f"""
        CREATE TABLE IF NOT EXISTS {casrec_mapping_schema}.cases (
            sirius_id int,
            "Order No" varchar
        )
        """,
        from_sql='SELECT id AS sirius_id, c_order_no AS "Order No" FROM integration.cases',
        to_table=f"{casrec_mapping_schema}.cases",
    )

    # Mapping from Sirius annual_report_type_assignments ID to migrated reporttype and type
    _copy(
        create_sql=f"""
        CREATE TABLE IF NOT EXISTS {casrec_mapping_schema}.annual_report_type_assignments (
            sirius_id int PRIMARY KEY,
            reporttype varchar,
            type varchar
        )
        """,
        from_sql="SELECT id AS sirius_id, reporttype, type FROM integration.annual_report_type_assignments",
        to_table=f"{casrec_mapping_schema}.annual_report_type_assignments",
    )

    # Mapping from Sirius annual_report_logs ID to migrated status
    _copy(
        create_sql=f"""
        CREATE TABLE IF NOT EXISTS {casrec_mapping_schema}.annual_report_logs (
            sirius_id int PRIMARY KEY,
            status varchar,
            reviewstatus varchar
        )
        """,
        from_sql="SELECT id AS sirius_id, status, reviewstatus FROM integration.annual_report_logs",
        to_table=f"{casrec_mapping_schema}.annual_report_logs",
    )


def delete_schema(schema_name, cursor, conn):
    sql = f"""
        DROP SCHEMA IF EXISTS {schema_name} CASCADE;
    """

    cursor.execute(sql)
    conn.commit()
    log.info(f"Dropped schema {schema_name}")


def run_post_migration_fix(script_path, dump_sql):
    """
    Run one post-migration fix script

    :param script_path: SQL script file to run
    :param dump_sql: True to print SQL to screen without running it
    """
    schema_name = (
        f'{get_pmf_schema_name(script_path)}{config.migration_phase["suffix"]}'
    )

    statements = {
        "setup": get_statements(script_path, "setup", schema_name),
        "audit": get_statements(script_path, "audit", schema_name),
        "update": get_statements(script_path, "update", schema_name),
        "validate": get_statements(script_path, "validate", schema_name),
    }

    # early return if dumping statements to screen
    if dump_sql:
        for key, statement_group in statements.items():
            print(f"{'*' * 50} {key}")
            for statement in statement_group:
                print(statement)
            print()
        return statements

    log.info(f"===== {schema_name} =====")

    connection_string = target_db_conn_string
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()
    log.info(f"Deleting existing schema")
    delete_schema(schema_name, cursor, conn)

    log.info(f"Running Setup Statements")
    for statement in setup_statements:
        cursor.execute(statement)

        if (
            "create schema" not in statement.lower()
            and "set datestyle" not in statement.lower()
        ):
            log.info(f"Setup inserted {cursor.rowcount} rows")
    conn.commit()

    log.info("Running Audit Statements")
    for statement in audit_statements:
        cursor.execute(statement)
        log.info(f"Audit inserted {cursor.rowcount} rows")
    conn.commit()

    log.info("Running Validation Statements Before Apply")
    for statement in validate_statements:
        cursor.execute(statement)
        log.info(f"Pre Validation bringing back {cursor.rowcount} rows")
        if cursor.rowcount < 1:
            log.warning("Nothing to apply here. Find out why!")
        else:
            pass
    conn.commit()

    rollback = False
    log.info("Running Update Statements")
    for statement in update_statements:
        cursor.execute(statement)
        log.info(f"Updated {cursor.rowcount} rows")
        if cursor.rowcount < 1:
            rollback = True
        else:
            pass

    log.info("Running Validation Statements After Apply")
    for statement in validate_statements:
        cursor.execute(statement)
        log.info(f"Post Validation bringing back {cursor.rowcount} rows")
        if cursor.rowcount > 0:
            rollback = True

    if rollback:
        log.info(f"Rolling back update transaction for {schema_name}")
        conn.rollback()
    else:
        log.info(f"Committing transaction for {schema_name}")
        conn.commit()

    cursor.close()


def run_post_migration_fixes():
    """
    Run all the post migration scripts in folders prefixed with two digits;
    for the purposes of ordering, each post-migration script should be within a numbered folder
    in format XX_pmf_*; within each folder, if the scripts need to run in a specific order, they
    should also be prefixed with two digits to signify the ordering.
    """

    this_dir = os.path.dirname(__file__)
    sql_dir = os.path.join(this_dir, "pmf_sql_statements/*/*.sql")
    sql_scripts = glob(sql_dir)
    sql_scripts = list(
        filter(
            lambda script_path: re.search(r"[\d]{2}_pmf", script_path) is not None,
            sql_scripts,
        )
    )
    sql_scripts = sorted(sql_scripts)

    for script_path in sql_scripts:
        run_post_migration_fix(script_path)


def get_statements(path, tag_prefix, pmf_schema):
    sql_statements = []
    sql_statement = ""
    with open(path, "r") as script:
        continue_adding_lines = False
        for line in script:

            if line.startswith(f"--@{tag_prefix}_tag"):
                continue_adding_lines = True
            elif line.startswith(f"--@"):
                continue_adding_lines = False
            else:
                pass

            if continue_adding_lines and not line.startswith("--") and len(line) > 0:
                line = line.strip().replace(
                    "{casrec_schema}", config.schemas["pre_transform"]
                )
                line = line.replace("{pmf_schema}", pmf_schema)
                line = line.replace(
                    "{client_source}", config.migration_phase["migration_identifier"]
                )
                line = line.replace("{casrec_mapping}", casrec_mapping_schema)
                if not line.endswith(";"):
                    sql_statement += f"{line}\n"
                else:
                    sql_statement += f"{line}\n"
                    sql_statements.append(sql_statement)
                    sql_statement = ""

    return sql_statements


def get_pmf_schema_name(script_path):
    script_path_parts = str(script_path).split("/")
    schema_name = str(script_path_parts[-2])[3:]
    return schema_name


def main(script_path=None, dump_sql=False):
    log.info(log_title(message="Run Post Migration Fixes"))

    copy_mapping_tables(casrec_mapping_schema)

    if script_path is None:
        run_post_migration_fixes()
    elif os.path.isfile(script_path):
        run_post_migration_fix(script_path, dump_sql)
    else:
        raise FileNotFoundError(f"{script_path} is not a file")


if __name__ == "__main__":
    t = time.process_time()

    log.setLevel(1)
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    script_path = None
    if len(sys.argv) > 1:
        script_path = sys.argv[1]

    dump_sql = False
    if len(sys.argv) > 2:
        dump_sql = sys.argv[2] == "dumpsql"

    main(script_path, dump_sql)

    print(f"Total time: {round(time.process_time() - t, 2)}")
