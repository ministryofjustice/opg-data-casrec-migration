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


class CountsVerification:

    report_columns = {}

    def __init__(self):
        self.fetch_existing_report_columns()


    def fetch_existing_report_columns(self):
        conn = conn_target['connection']
        try:
            cursor = conn.cursor()
            query = "SELECT column_name FROM information_schema.columns " \
                    "WHERE table_schema = 'countverification' " \
                    "AND table_name = 'counts';"
            cursor.execute(query)
            for col in cursor.fetchall():
                self.add_report_column(col[0])
        except (Exception, psycopg2.DatabaseError) as error:
            log.error("Error: %s" % error)
        finally:
            cursor.close()


    def add_report_column(self, col_name):
        self.report_columns[col_name] = col_name.replace('_', ' ').title()


    def reset_schema(self):
        log.info(f"Resetting countverification schema on {conn_target['name']}")
        execute_sql_file(sql_path, "schema_down.sql", conn_target['connection'])
        self.create_schema()


    def create_schema(self):
        execute_sql_file(sql_path, "schema_up.sql", conn_target['connection'])
        self.report_columns = {}
        self.add_report_column("supervision_table")


    def check_schema(self):
        if not schema_exists(
            conn=conn_target['connection'],
            schema=config.schemas['count_verification']
        ):
            self.create_schema()


    def count_cp1_data(self, calling_stage):
        log.info(f"Count CP1 Supervision data on {conn_target['name']} ({calling_stage})")
        col = "cp1_" + calling_stage
        execute_sql_template(
            conn=conn_target['connection'],
            template_filename="count_cp1.sql",
            replace_tags={"working_column": col}
        )
        self.add_report_column(col)


    def count_non_cp1_data(self, calling_stage):
        log.info(f"Count Non-CP1 Supervision data on {conn_target['name']} ({calling_stage})")
        col = "non_cp1_" + calling_stage
        execute_sql_template(
            conn=conn_target['connection'],
            template_filename="count_non_cp1.sql",
            replace_tags={"working_column": col}
        )
        self.add_report_column(col)


    def count_non_supervision(self, calling_stage):
        log.info(f"Count Non-Supervision data on {conn_target['name']} ({calling_stage})")
        col = "lay_" + calling_stage
        execute_sql_template(
            conn=conn_target['connection'],
            template_filename="count_non_supervision.sql",
            replace_tags={"working_column": col}
        )
        self.add_report_column(col)


    def count_casrec_source(self, calling_stage):
        log.info(f"Count Casrec data on {conn_migration['name']} ({calling_stage})")

        copy_schema(
            log=log,
            sql_path=current_path / "../../shared/sql",
            config=config,
            from_db="target",
            from_schema=config.schemas["count_verification"],
            to_db="migration",
            to_schema=config.schemas["count_verification"],
        )

        col = "casrec_" + calling_stage
        execute_sql_template(
            conn=conn_migration['connection'],
            template_filename="count_casrec_source.sql",
            replace_tags={"working_column": col}
        )

        copy_schema(
            log=log,
            sql_path=current_path / "../../shared/sql",
            config=config,
            from_db="migration",
            from_schema=config.schemas["count_verification"],
            to_db="target",
            to_schema=config.schemas["count_verification"],
        )

        self.add_report_column(col)


    def calculate_result(self):
        execute_sql_template(
            conn=conn_target['connection'],
            template_filename="calculate_result.sql",
            replace_tags={}
        )
        self.add_report_column("result")


    def output_report(self):
        cols = ",".join(self.report_columns.keys())
        df = pd.read_sql(
            sql=f"SELECT {cols} FROM countverification.counts ORDER BY supervision_table;",
            con=conn_target['connection']
        )
        report_table = tabulate(
            df,
            list(self.report_columns.values()),
            tablefmt="psql"
        )
        print(report_table)


    def do_pre_delete(self):
        self.reset_schema()
        self.count_cp1_data('pre_delete')
        self.count_non_cp1_data('pre_delete')
        self.count_non_supervision('pre_delete')
        self.output_report()


    def do_post_delete(self):
        self.check_schema()
        self.count_cp1_data('post_delete')
        self.count_non_cp1_data('post_delete')
        self.count_non_supervision('post_delete')
        self.output_report()


    def do_pre_migration(self):
        self.check_schema()
        self.count_casrec_source('pre_migrate')
        self.output_report()


    def do_post_migration(self):
        self.check_schema()
        self.count_cp1_data('post_migrate')
        self.count_non_supervision('post_migrate')
        self.calculate_result()
        self.output_report()


    def call_stage(self, stage: str):
        do = f"do_{stage}"
        if hasattr(self, do) and callable(func := getattr(self, do)):
            log.info(f"Stage: {stage}")
            func()
        else:
            print(f"stage {stage} not recognised")
