import os
import sys
from pathlib import Path

from clear_database import empty_target_tables
from move import generate_inserts
from setup import insert_base_data


current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")


import logging
import time
import click
from sqlalchemy import create_engine
import custom_logger
from helpers import log_title
import table_helpers

from dotenv import load_dotenv


# set config
current_path = Path(os.path.dirname(os.path.realpath(__file__)))
env_path = current_path / "../../.env"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
import helpers

config = helpers.get_config(env=environment)

# logging
# custom_logger.custom_log_level(levels=config.custom_log_levels)
config.custom_log_level()
verbosity_levels = config.verbosity_levels
log = logging.getLogger("root")
log.addHandler(custom_logger.MyHandler())

# database
db_config = {
    "db_connection_string": config.get_db_connection_string("migration"),
    "source_schema": config.schemas["integration"],
    "target_schema": config.schemas["pre_migration"],
}
target_db_engine = create_engine(db_config["db_connection_string"])


@click.command()
@click.option("-v", "--verbose", count=True)
@click.option(
    "--clear",
    prompt=False,
    default=False,
    help="Clear existing database tables: True or False",
)
def main(verbose, clear):
    try:
        log.setLevel(verbosity_levels[verbose])
        log.info(f"{verbosity_levels[verbose]} logging enabled")
    except KeyError:
        log.setLevel("INFO")
        log.info(f"{verbose} is not a valid verbosity level")
        log.info(f"INFO logging enabled")

    log.info(log_title(message="Integration Step: Load to Staging"))
    log.info(
        log_title(
            message=f"Source: {db_config['source_schema']} Target: {db_config['target_schema']}"
        )
    )
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")
    tables_list = table_helpers.get_table_list(table_helpers.get_table_file())

    if clear:
        empty_target_tables(
            db_config=db_config, db_engine=target_db_engine, tables=tables_list[:]
        )

    insert_base_data(db_config=db_config, db_engine=target_db_engine)

    generate_inserts(
        db_config=db_config, db_engine=target_db_engine, tables=tables_list
    )


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
