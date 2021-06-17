import os
import sys
from pathlib import Path
import logging
import time
import click
from sqlalchemy import create_engine

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")
from existing_data.match_existing_data import match_existing_data
from reindex.move_by_table import move_all_tables, create_schema
from reindex.reindex_foreign_keys import update_fks
from reindex.reindex_primary_keys import update_pks
from utilities.clear_database import clear_tables


from quick_validation import check_row_counts

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


# database
db_config = {
    "db_connection_string": config.get_db_connection_string("migration"),
    "sirius_db_connection_string": config.get_db_connection_string("target"),
    "source_schema": config.schemas["post_transform"],
    "target_schema": config.schemas["integration"],
    "sirius_schema": config.schemas["public"],
    "chunk_size": config.DEFAULT_CHUNK_SIZE,
}
target_db_engine = create_engine(db_config["db_connection_string"])

# logging
log = logging.getLogger("root")
custom_logger.setup_logging(
    env=environment, db_config=db_config, module_name="reindex ids"
)


@click.command()
@click.option("--team", default="")
@click.option(
    "--clear",
    prompt=False,
    default=False,
    help="Clear existing database tables: True or False",
)
def main(clear, team):

    allowed_entities = config.allowed_entities(env=os.environ.get("ENVIRONMENT"))

    log.info(
        log_title(message="Integration Step: Reindex migrated data based on Sirius ids")
    )
    log.info(log_title(message=f"Team: {team}"))
    log.info(
        log_title(
            message=f"Source: {db_config['source_schema']}, Target: {db_config['target_schema']}, Chunk Size: {db_config['chunk_size']}"
        )
    )
    log.info(log_title(message=f"Enabled entities: {', '.join(allowed_entities)}"))
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    log.info(f"Creating schema '{db_config['target_schema']}' if it doesn't exist")
    create_schema(
        target_db_connection=db_config["db_connection_string"],
        schema_name=db_config["target_schema"],
    )

    if clear:
        clear_tables(db_config)

    enabled_tables = table_helpers.get_enabled_table_details()
    if "additional_data" not in allowed_entities:

        log.info("additional_data entity not enabled, exiting")
        enabled_extra_tables = {}

    else:
        enabled_extra_tables = table_helpers.get_enabled_table_details(
            file_name="additional_data_tables"
        )

    all_enabled_tables = {**enabled_tables, **enabled_extra_tables}

    log.info(
        f"Moving data from '{db_config['source_schema']}' schema to '{db_config['target_schema']}' schema"
    )
    move_all_tables(db_config=db_config, table_list=all_enabled_tables)

    log.info(f"Merge new data with existing data in Sirius")
    match_existing_data(db_config=db_config, table_details=all_enabled_tables)

    log.info(f"Reindex all primary keys")
    update_pks(db_config=db_config, table_details=enabled_tables)
    log.info(f"Reindex all foreign keys")
    update_fks(db_config=db_config, table_details=all_enabled_tables)

    if environment == "local":
        check_row_counts.count_rows(
            connection_string=db_config["db_connection_string"],
            destination_schema=db_config["target_schema"],
            enabled_entities=allowed_entities,
            team=team,
        )


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
