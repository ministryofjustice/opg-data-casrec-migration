import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import logging.config
import time
import psycopg2
import custom_logger
from dotenv import load_dotenv
import click
import helpers
from db_helpers import copy_schema
from db_helpers import execute_sql_file
from db_helpers import schema_exists
from helpers import log_title
import pandas as pd
from tabulate import tabulate

env_path = current_path / "../../.env"
load_dotenv(dotenv_path=env_path)
environment = os.environ.get("ENVIRONMENT")
config = helpers.get_config(env=environment)

custom_logger.setup_logging(
    env=environment,
    module_name="Count client-pilot-one data",
)
log = logging.getLogger("root")
config.custom_log_level()

conn_migration = psycopg2.connect(config.get_db_connection_string("migration"))
conn_target = psycopg2.connect(config.get_db_connection_string("target"))

def output_title(correfs):
    allowed_entities = config.allowed_entities(env=environment)
    filtered_correfs = config.get_filtered_correfs(environment, correfs)
    log.info(log_title(message="Counts Verification: Pre-Migration counts"))
    log.debug(f"Environment: {environment}")
    log.info(f"Correfs: {', '.join(filtered_correfs) if filtered_correfs else 'all'}")
    log.info(f"Enabled entities: {', '.join(allowed_entities)}")
    log.info(
        f"Enabled features: {', '.join(config.enabled_feature_flags(environment))}"
    )
    log.info(log_title(message="Begin"))


def count_non_cp1():
    log.info("Step 1/4: Count Non-Client-Pilot-One data on target")
    execute_sql_file(current_path / "sql", "count_non_cp1.sql", conn_target)


def count_existing_cp1():
    log.info("Step 2/4: Count Existing Client-Pilot-One data on target")
    execute_sql_file(current_path / "sql", "count_existing_cp1.sql", conn_target)


def count_casrec_source():
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

    execute_sql_file(current_path / "sql", "count_casrec_source.sql", conn_migration)
    log.info(f"Updated count record with source data counts.")


@click.command()
@click.option("--correfs", default="")
def main(correfs):
    output_title(correfs)
    count_existing_cp1()

    if not schema_exists(
        conn=conn_target,
        schema=config.schemas['count_verification']
    ):
        log.error(f"{config.schemas['count_verification']} schema not found in target DB")
        log.info(f"Skipping remainder of counts verification.")
    else:
        count_non_cp1()
        count_casrec_source()

    df = pd.read_sql(
        sql="SELECT * FROM countverification.counts ORDER BY supervision_table;",
        con=conn_migration
    )
    headers = ["Supervision Table", "CP1 Existing", "Non-CP1 Remaining", "Casrec"]
    report_table = tabulate(df, headers, tablefmt="psql")
    print(report_table)


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
