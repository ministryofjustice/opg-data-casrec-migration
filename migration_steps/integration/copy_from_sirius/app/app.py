import os
import sys
from pathlib import Path

from utilities.copy_tables import copy_tables
from utilities.clear_tables import clear_tables

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import logging
import time
import click
from sqlalchemy import create_engine
import custom_logger
from helpers import log_title
from table_helpers import get_table_file

from dotenv import load_dotenv


# set config
current_path = Path(os.path.dirname(os.path.realpath(__file__)))
env_path = current_path / "../../.env"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
import helpers


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
source_db_engine = create_engine(db_config["sirius_db_connection_string"])
target_db_engine = create_engine(db_config["db_connection_string"])

# logging
log = logging.getLogger("root")
custom_logger.setup_logging(
    env=environment, db_config=db_config, module_name="copy from Sirius"
)


@click.command()
@click.option("--correfs", default="")
@click.option(
    "--clear",
    prompt=False,
    default=False,
    help="Clear existing database tables: True or False",
)
def main(clear, correfs):
    allowed_entities = config.allowed_entities(env=os.environ.get("ENVIRONMENT"))
    filtered_correfs = config.get_filtered_correfs(environment, correfs)

    log.info(log_title(message="Integration Step: Copy Sirius data into Staging DB"))
    log.info(log_title(message=f"Correfs: {', '.join(filtered_correfs) if filtered_correfs else 'all'}"))
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

    tables_to_copy = get_table_file(file_name="tables_to_copy_from_sirius")

    if clear:
        clear_tables(
            db_engine=target_db_engine, db_config=db_config, tables=tables_to_copy
        )

    copy_tables(
        db_config=db_config,
        source_db_engine=source_db_engine,
        target_db_engine=target_db_engine,
        tables=tables_to_copy,
    )


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
