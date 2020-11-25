import sys
import os
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")

import logging
import time
import click
from sqlalchemy import create_engine
import custom_logger
from helpers import log_title
from config import get_config
from dotenv import load_dotenv

from run_data_tests import run_data_tests
from entities import clients, cases, supervision_level
from utilities.clear_database import clear_tables
from utilities.db_insert import InsertData

# set config
current_path = Path(os.path.dirname(os.path.realpath(__file__)))
env_path = current_path / "../.env"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
config = get_config(env=environment)

# logging
log = logging.getLogger("root")
log.addHandler(custom_logger.MyHandler())

config.custom_log_level()
verbosity_levels = config.verbosity_levels

# database

etl2_db_engine = create_engine(config.connection_string)

etl2_db = InsertData(db_engine=etl2_db_engine, schema=config.etl2_schema)


@click.command()
@click.option(
    "--clear",
    prompt=False,
    default=False,
    help="Clear existing database tables: True or False",
)
@click.option(
    "--entity_list",
    multiple=True,
    prompt=False,
    help="List of entities you want to transform, eg 'clients,deputies,cases'.",
)
@click.option(
    "--include_tests",
    help="Run data tests after performing the transformations",
    default=False,
)
@click.option("-v", "--verbose", count=True)
def main(clear, entity_list, include_tests, verbose):
    try:
        log.setLevel(verbosity_levels[verbose])
        log.info(f"{verbosity_levels[verbose]} logging enabled")
    except KeyError:
        log.setLevel("INFO")
        log.info(f"{verbose} is not a valid verbosity level")
        log.info(f"INFO logging enabled")

    log.info(log_title(message="Migration Step: Transform Casrec Data"))
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    if clear:
        clear_tables(config)

    if entity_list:
        allowed_entities = (entity_list)[0].split(",")
        log.info(f"Processing list of entities: {(', ').join(entity_list)}")

    else:
        allowed_entities = []
        log.info("Processing all entities")

    # Data - each entity can be run independently
    if len(allowed_entities) == 0 or "clients" in allowed_entities:
        clients.runner(config, etl2_db)

    if len(allowed_entities) == 0 or "cases" in allowed_entities:
        cases.runner(config, etl2_db)

    if len(allowed_entities) == 0 or "supervision_level" in allowed_entities:
        supervision_level.runner(config, etl2_db)

    if include_tests:
        run_data_tests(verbosity_level=verbosity_levels[verbose])


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
