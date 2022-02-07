import os
import sys
from pathlib import Path
import pandas as pd
from tabulate import tabulate
import psycopg2
import logging.config
from dotenv import load_dotenv

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import helpers
from db_helpers import execute_sql_file
from db_helpers import create_from_template
from db_helpers import copy_schema
from db_helpers import schema_exists

env_path = current_path / "../../.env"
sql_path = current_path / "sql"
load_dotenv(dotenv_path=env_path)
environment = os.environ.get("ENVIRONMENT")
config = helpers.get_config(env=environment)
log = logging.getLogger("root")

conn_migration = {
    'name': 'casrecmigration',
    'connection': psycopg2.connect(config.get_db_connection_string("migration"))
}
conn_target = {
    'name': 'sirius',
    'connection': psycopg2.connect(config.get_db_connection_string("target"))
}

def count_final():
    if not schema_exists(
        conn=conn_migration,
        schema=config.schemas['count_verification']
    ):
        log.error(f"This step requires Counts Verification Step 2/3 - count Casrec data")
        log.info(f"{config.schemas['count_verification']} schema not found in casrecmigration DB")
        log.info(f"Aborting.")
    else:

        log.info(f"Copy {config.schemas['count_verification']} schema to target DB")
        copy_schema(
            log=log,
            sql_path=current_path / "../../shared/sql",
            config=config,
            from_db="migration",
            from_schema=config.schemas["count_verification"],
            to_db="target",
            to_schema=config.schemas["count_verification"],
        )

        execute_sql_file(sql_path, "count_final.sql", conn_target)
        log.info(f"Updated count record with final counts form Sirius")

        df = pd.read_sql(
            sql = "SELECT * FROM countverification.counts ORDER BY supervision_table;",
            con=conn_target
        )
        headers = ["Supervision Table", "CP1 Existing", "Non-CP1 Remaining", "Casrec", "Expected", "Final Count", "Result"]
        report_table = tabulate(df, headers, tablefmt="psql")
        print(report_table)


def count_non_supervision():
    log.info("Count Non-Supervision data on target")


def count_casrec_source():
    if not schema_exists(
            conn=conn_target,
            schema=config.schemas['count_verification']
    ):
        log.error(f"{config.schemas['count_verification']} schema not found in target DB")
        log.info(f"Skipping remainder of counts verification.")
    else:
        log.info("Step 3/4: Count Casrec source data")
        log.info(f"Copy {config.schemas['count_verification']} schema to casrecmigration DB")
        copy_schema(
            log=log,
            sql_path=current_path / "../../shared/sql",
            config=config,
            from_db="target",
            from_schema=config.schemas["count_verification"],
            to_db="migration",
            to_schema=config.schemas["count_verification"],
        )

        execute_sql_file(sql_path, "count_casrec_source.sql", conn_migration)
        log.info(f"Updated count record with source data counts.")

        df = pd.read_sql(
            sql="SELECT * FROM countverification.counts ORDER BY supervision_table;",
            con=conn_migration
        )

        headers = ["Supervision Table", "CP1 Existing", "Non-CP1 Remaining", "Casrec"]
        report_table = tabulate(df, headers, tablefmt="psql")
        print(report_table)


def count_cp1_data(conn, working_column):
    log.info(f"Count CP1 Supervision data on {conn['name']} ({working_column})")
    execute_sql_template(
        conn = conn['connection'],
        template_filename = "count_cp1.sql",
        replace_tags = {"working_column": "cp1_" + working_column}
    )


def execute_sql_template(conn, template_filename, replace_tags):
    template = open(sql_path / template_filename, "r")
    execution_filename = "execute_"+template_filename
    execution_file = open(sql_path / execution_filename, "w+")

    for line in template:
        for check, rep in replace_tags.items():
            line = line.replace("{" + check + "}", rep)
        execution_file.write(line)
    template.close()

    execution_file.seek(0, 0)

    cursor = conn.cursor()
    try:
        cursor.execute(execution_file.read())
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        execution_file.close()
    cursor.close()
    execution_file.close()
    os.remove(sql_path / execution_filename)


def count_non_cp1_data():
    log.info("Count Non-CP1 Supervision data on target")
    # execute_sql_file(sql_path, "count_non_cp1.sql", conn_target)


def reset_schema(conn):
    log.info(f"Resetting countverification schema on {conn['name']}")
    execute_sql_file(sql_path, "reset_schema.sql", conn['connection'])


class CountsVerification:

    def do_pre_delete(self):
        reset_schema(conn_migration)
        reset_schema(conn_target)
        count_cp1_data(conn_target, 'pre_delete')
        # count_non_supervision()


    def do_post_delete(self):
        count_cp1_data(conn_target, 'post_delete')
        # count_non_supervision()
        # count_non_cp1_data()


    def do_pre_migration(self):
        count_casrec_source()


    def do_post_migration(self):
        count_final()


    def call_stage(self, stage: str):
        do = f"do_{stage}"
        if hasattr(self, do) and callable(func := getattr(self, do)):
            log.info(f"Stage: {stage}")
            func()
        else:
            print(f"stage {stage} not recognised")
