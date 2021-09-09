import os
import sys
from pathlib import Path


current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

from clear import clear_tables
from insert_additional_data import insert_additional_data_records

# from insert_2 import insert_additional_data_records
import logging
import time
import click

import custom_logger
from helpers import log_title
import helpers
from decorators import timer, mem_tracker

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
    "source_schema": config.schemas["pre_transform"],
    "target_schema": config.schemas["post_transform"],
    "chunk_size": config.DEFAULT_CHUNK_SIZE,
}


allowed_entities = config.allowed_entities(env=os.environ.get("ENVIRONMENT"))


@click.command()
@click.option(
    "--clear",
    prompt=False,
    default=False,
    help="Clear existing database tables: True or False",
)
@mem_tracker
@timer
def main(clear):

    allowed_entities = config.allowed_entities(env=os.environ.get("ENVIRONMENT"))

    log.info(log_title(message="Migration Step: additional_data"))
    log.info(
        log_title(
            message=f"Source: {db_config['source_schema']}, Target: {db_config['target_schema']}, Chunk Size: {db_config['chunk_size']}"
        )
    )
    log.info(log_title(message=f"Enabled entities: {', '.join(allowed_entities)}"))
    log.info(
        log_title(
            message=f"Enabled features: {', '.join(config.enabled_feature_flags(env=os.environ.get('ENVIRONMENT')))}"
        )
    )

    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")
    version_details = helpers.get_json_version()
    log.info(
        f"Using JSON def version '{version_details['version_id']}' last updated {version_details['last_modified']}"
    )

    if "additional-data" not in config.enabled_feature_flags(env=environment):
        log.info("additional-data flag not enabled, exiting")
        return False

    all_files = [x[:-5] for x in helpers.get_all_additional_data_files()]

    if clear:
        clear_tables(db_config=db_config, files=all_files)

    for file in all_files:
        insert_additional_data_records(
            db_config=db_config, additional_data_file_name=file
        )


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
