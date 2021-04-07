import os
import sys
from pathlib import Path

# from utilities.progress import update_progress

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")

from decorators import files_used
from progress import update_progress
import logging
import time
import click
from sqlalchemy import create_engine
import custom_logger
from helpers import log_title
import helpers
from decorators import timer, mem_tracker

from dotenv import load_dotenv

from run_data_tests import run_data_tests
from entities import (
    clients,
    cases,
    supervision_level,
    deputies,
    bonds,
    death,
    events,
    finance,
    remarks,
    reporting,
    tasks,
    teams,
    visits,
    warnings,
)
from utilities.clear_database import clear_tables
from utilities.db_insert import InsertData

# set config
current_path = Path(os.path.dirname(os.path.realpath(__file__)))
env_path = current_path / "../../.env"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")


config = helpers.get_config(env=environment)

# logging
log = logging.getLogger("root")
custom_logger.setup_logging(env=environment)


# database
db_config = {
    "db_connection_string": config.get_db_connection_string("migration"),
    "source_schema": config.schemas["pre_transform"],
    "target_schema": config.schemas["post_transform"],
}

allowed_entities = [k for k, v in config.ENABLED_ENTITIES.items() if v is True]


target_db_engine = create_engine(db_config["db_connection_string"])
target_db = InsertData(db_engine=target_db_engine, schema=db_config["target_schema"])


@click.command()
@click.option(
    "--clear",
    prompt=False,
    default=False,
    help="Clear existing database tables: True or False",
)
@click.option(
    "--include_tests",
    help="Run data tests after performing the transformations",
    default=False,
)
@click.option(
    "--chunk_size",
    prompt=False,
    type=int,
    help="Defaults to 10,000 but can be changed for dev",
    default=10000,
)
@mem_tracker
@timer
def main(clear, include_tests, chunk_size):

    log.info(log_title(message="Migration Step: Transform Casrec Data"))
    log.info(
        log_title(
            message=f"Source: {db_config['source_schema']} Target: {db_config['target_schema']}"
        )
    )
    log.info(
        log_title(
            message=f"Enabled entities: {', '.join(k for k, v in config.ENABLED_ENTITIES.items() if v is True)}"
        )
    )
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")
    version_details = helpers.get_json_version()
    log.info(
        f"Using JSON def version '{version_details['version_id']}' last updated {version_details['last_modified']}"
    )

    db_config["chunk_size"] = chunk_size if chunk_size else 10000
    log.info(f"Chunking data at {chunk_size} rows")
    print(f"allowed_entities: {allowed_entities}")

    if clear:
        clear_tables(db_config=db_config)

    clients.runner(target_db=target_db, db_config=db_config)
    cases.runner(target_db=target_db, db_config=db_config)
    bonds.runner(target_db=target_db, db_config=db_config)
    supervision_level.runner(target_db=target_db, db_config=db_config)
    deputies.runner(target_db=target_db, db_config=db_config)
    death.runner(target_db=target_db, db_config=db_config)
    events.runner(target_db=target_db, db_config=db_config)
    finance.runner(target_db=target_db, db_config=db_config)
    remarks.runner(target_db=target_db, db_config=db_config)
    reporting.runner(target_db=target_db, db_config=db_config)
    tasks.runner(target_db=target_db, db_config=db_config)
    teams.runner(target_db=target_db, db_config=db_config)
    visits.runner(target_db=target_db, db_config=db_config)
    warnings.runner(target_db=target_db, db_config=db_config)

    if include_tests:
        run_data_tests(verbosity_level="DEBUG")

    if environment == "local":
        update_progress(module_name="transform", completed_items=files_used)
        log.debug(f"Number of mapping docs used: {len(files_used)}")


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
