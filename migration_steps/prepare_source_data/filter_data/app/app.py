import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import time
import psycopg2
from helpers import get_config
from dotenv import load_dotenv
from helpers import log_title
from db_helpers import *
import logging
import custom_logger
import click

env_path = current_path / "../../../../.env"
sql_path = current_path / "sql"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
config = get_config(environment)

# logging
log = logging.getLogger("root")
log.addHandler(custom_logger.MyHandler())
config.custom_log_level()
verbosity_levels = config.verbosity_levels


def set_logging_level(verbose):
    try:
        log.setLevel(verbosity_levels[verbose])
    except KeyError:
        log.setLevel("INFO")
        log.info(f"{verbose} is not a valid verbosity level")


@click.command()
@click.option("-v", "--verbose", count=True)
@click.option("--correfs", default="")
@click.option("--clear", prompt=False, default=False)
def main(verbose, correfs, clear):
    set_logging_level(verbose)
    log.info(log_title(message="Filter Data"))

    log.info("Creating cases_to_filter_out table in pre_transform schema")
    sql = f"""
        DROP TABLE IF EXISTS {config.schemas["pre_transform"]}.cases_to_filter_out;
        CREATE TABLE {config.schemas["pre_transform"]}.cases_to_filter_out (
            caserecnumber text,
            notes text
        );
    """
    conn_source = psycopg2.connect(config.get_db_connection_string("migration"))
    cursor_source = conn_source.cursor()
    cursor_source.execute(sql)
    conn_source.commit()
    log.info("Getting CLIENT-PILOT-ONE cases from target")
    sql = "SELECT caserecnumber FROM public.persons WHERE caseactorgroup = 'CLIENT-PILOT-ONE';"
    conn_target = psycopg2.connect(config.get_db_connection_string("target"))
    cursor_target = conn_target.cursor()
    cursor_target.execute(sql)
    pilot_cases = cursor_target.fetchall()
    cursor_target.close()

    if pilot_cases:
        log.info(
            f"Inserting {len(pilot_cases)} CLIENT-PILOT-ONE cases into cases_to_filter_out table"
        )
        values = [f"('{case[0]}', 'pilot')" for case in pilot_cases]
        sql = f"""
            INSERT INTO {config.schemas["pre_transform"]}.cases_to_filter_out (caserecnumber, notes)
            VALUES {", ".join(values)};
        """
        cursor_source.execute(sql)
    else:
        log.info("No CLIENT-PILOT-ONE cases found in target")

    filtered_correfs = config.get_filtered_correfs(environment, correfs)

    if filtered_correfs:
        log.info(
            f"Inserting cases not associated with Correfs: ({', '.join(filtered_correfs)}) into cases_to_filter_out table"
        )
        sql = f"""
            INSERT INTO {config.schemas["pre_transform"]}.cases_to_filter_out (caserecnumber, notes)
            SELECT "Case", CONCAT('Corref: ', "Corref")
            FROM {config.schemas["pre_transform"]}.pat
            WHERE "Corref" NOT IN ({",".join([f"'{corref}'" for corref in filtered_correfs])});
        """
        cursor_source.execute(sql)
    else:
        log.info("No Corref filtering requested")

    cursor_source.close()
    conn_source.commit()

    if pilot_cases or filtered_correfs:
        log.info(f"Deleting data associated with cases in cases_to_filter_out table")
        execute_sql_file(
            sql_path,
            "delete_filtered_source_data.sql",
            conn_source,
            casrec_schema=config.migration_phase["casrec_schema"],
        )
    else:
        log.info("Nothing to delete from source data")


if __name__ == "__main__":
    t = time.process_time()

    log.setLevel(1)
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
