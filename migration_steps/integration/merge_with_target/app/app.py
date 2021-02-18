import os
import sys
from pathlib import Path


from utilities.clear_database import clear_tables
from utilities.db_insert import InsertData
from utilities.move_by_table import move_a_table, move_all_tables

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")
from entities import client, supervision_level, cases, deputies

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
    "sirius_db_connection_string": config.get_db_connection_string("target"),
    "source_schema": config.schemas["post_transform"],
    "target_schema": config.schemas["integration"],
    "sirius_schema": config.schemas["public"],
}
target_db_engine = create_engine(db_config["db_connection_string"])
target_db = InsertData(db_engine=target_db_engine, schema=db_config["target_schema"])


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

    log.info(log_title(message="Integration Step: Merge Casrec data with Sirius data"))
    log.info(
        log_title(
            message=f"Source: {db_config['source_schema']} Target: {db_config['target_schema']}"
        )
    )
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    if clear:
        clear_tables(db_config)

    log.info(
        f"Moving data from '{db_config['source_schema']}' schema to '{db_config['target_schema']}' schema and reindexing pks"
    )
    # tables_list = table_helpers.get_table_list(
    #     table_helpers.get_table_file()
    # )

    table_details = table_helpers.get_table_file()

    move_all_tables(db_config=db_config, target_db=target_db, table_list=table_details)

    # for table in tables_list:
    #     move_a_table(db_config=db_config, target_db=target_db, table_name=table)

    log.info(f"Joining entities together with fks")
    # client.merge_source_data(db_config=db_config, target_db=target_db)
    # cases.merge_source_data(db_config=db_config, target_db=target_db)
    # supervision_level.merge_source_data(db_config=db_config, target_db=target_db)
    # deputies.merge_source_data(db_config=db_config, target_db=target_db)


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
