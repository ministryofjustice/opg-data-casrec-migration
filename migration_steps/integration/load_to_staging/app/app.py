import os
import sys
import threading
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")
from clear_database import empty_target_tables
from move import generate_inserts, completed_tables
from setup import insert_base_data


from quick_validation import check_row_counts

import logging
import time
import click
from sqlalchemy import create_engine
import custom_logger
from helpers import log_title
from progress import update_progress
import table_helpers

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
    "source_schema": config.schemas["integration"],
    "target_schema": config.schemas["pre_migration"],
    "chunk_size": config.DEFAULT_CHUNK_SIZE,
}
target_db_engine = create_engine(db_config["db_connection_string"])

# logging
log = logging.getLogger("root")
custom_logger.setup_logging(
    env=environment, db_config=db_config, module_name="load to staging"
)


result = None


allowed_entities = config.allowed_entities(env=os.environ.get("ENVIRONMENT"))
tables_list = table_helpers.get_table_list(table_helpers.get_table_file())

enabled_tables = table_helpers.get_enabled_table_details()
if "additional_data" not in allowed_entities:

    log.info("additional_data entity not enabled, exiting")
    enabled_extra_tables = {}

else:
    enabled_extra_tables = table_helpers.get_enabled_table_details(
        file_name="additional_data_tables"
    )

all_enabled_tables = {**enabled_tables, **enabled_extra_tables}


def clear_tables():
    empty_target_tables(
        db_config=db_config,
        db_engine=target_db_engine,
        tables=tables_list[:],
        extra_tables=enabled_extra_tables,
    )

    global result
    result = "empty_target_tables complete"


def base_data():
    insert_base_data(db_config=db_config, db_engine=target_db_engine)
    global result
    result = "base_data complete"


def inserts():
    generate_inserts(
        db_config=db_config,
        db_engine=target_db_engine,
        tables=enabled_tables,
        extra_tables=enabled_extra_tables,
    )
    global result
    result = "inserts complete"


def update():
    update_progress(module_name="load_to_staging", completed_items=completed_tables)
    global result
    result = "update complete"


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

    log.info(log_title(message="Integration Step: Load to Staging"))
    log.info(log_title(message=f"Team: {team}"))
    log.info(
        log_title(
            message=f"Source: {db_config['source_schema']}, Target: {db_config['target_schema']}, Chunk Size: {db_config['chunk_size']}"
        )
    )
    log.info(log_title(message=f"Enabled entities: {', '.join(allowed_entities)}"))
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    work = [base_data, inserts]

    if clear:
        work.insert(0, clear_tables)
    if environment == "local":
        work.append(update)

    for item in work:
        thread = threading.Thread(target=item)
        thread.start()
        thread.join()
        log.debug(f"Result: {result}")

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
