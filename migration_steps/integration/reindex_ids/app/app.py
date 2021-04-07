import os
import sys
from pathlib import Path
import logging
import time
import click
from sqlalchemy import create_engine
from existing_data.match_existing_data import match_existing_data
from reindex.move_by_table import move_all_tables, create_schema
from reindex.reindex_foreign_keys import update_fks
from reindex.reindex_primary_keys import update_pks
from utilities.clear_database import clear_tables

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")


import custom_logger
import helpers
from helpers import log_title
import table_helpers

from dotenv import load_dotenv


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
    "sirius_db_connection_string": config.get_db_connection_string("target"),
    "source_schema": config.schemas["post_transform"],
    "target_schema": config.schemas["integration"],
    "sirius_schema": config.schemas["public"],
}
target_db_engine = create_engine(db_config["db_connection_string"])


@click.command()
@click.option(
    "--clear",
    prompt=False,
    default=False,
    help="Clear existing database tables: True or False",
)
def main(clear):

    log.info(
        log_title(message="Integration Step: Reindex migrated data based on Sirius ids")
    )
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

    log.info(f"Creating schema '{db_config['target_schema']}' if it doesn't exist")
    create_schema(
        target_db_connection=db_config["db_connection_string"],
        schema_name=db_config["target_schema"],
    )

    if clear:
        clear_tables(db_config)

    table_details = table_helpers.get_enabled_table_details()

    log.info(
        f"Moving data from '{db_config['source_schema']}' schema to '{db_config['target_schema']}' schema"
    )
    move_all_tables(db_config=db_config, table_list=table_details)

    log.info(f"Merge new data with existing data in Sirius")
    match_existing_data(db_config=db_config, table_details=table_details)

    log.info(f"Reindex all primary keys")
    update_pks(db_config=db_config, table_details=table_details)
    log.info(f"Reindex all foreign keys")
    update_fks(db_config=db_config, table_details=table_details)


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
