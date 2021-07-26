import json
import os
import sys
from pathlib import Path

from move import insert_data_into_target
from move import update_data_in_target

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

from audit import run_audit
import logging.config
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
    "source_db_connection_string": config.get_db_connection_string("migration"),
    "target_db_connection_string": config.get_db_connection_string("target"),
    "source_schema": config.schemas["pre_migration"],
    "target_schema": config.schemas["public"],
    "chunk_size": config.DEFAULT_CHUNK_SIZE,
}
source_db_engine = create_engine(db_config["source_db_connection_string"])
target_db_engine = create_engine(db_config["target_db_connection_string"])

# logging
log = logging.getLogger("root")
custom_logger.setup_logging(
    env=environment, db_config=db_config, module_name="load to sirius"
)

completed_tables = []


@click.command()
@click.option("-a", "--audit", count=False)
def main(audit):
    log.info(log_title(message="Load to Target Step: AKA do the migration already"))
    log.info(
        log_title(
            message=f"Source: {db_config['source_schema']}, Target: {db_config['target_schema']}, Chunk Size: {db_config['chunk_size']}"
        )
    )
    log.info(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    tables_dict = table_helpers.get_enabled_table_details()
    tables_list = table_helpers.get_table_list(tables_dict)

    if audit == "True":
        log.info(f"Running Pre-Audit - Table Copies")
        run_audit(target_db_engine, source_db_engine, "before", log, tables_list)
        log.info(f"Finished Pre-Audit - Table Copies")

    for i, table in enumerate(tables_list):

        log.debug(f"This is table number {i + 1} of {len(tables_list)}")

        insert_data_into_target(
            db_config=db_config,
            source_db_engine=source_db_engine,
            target_db_engine=target_db_engine,
            table_name=table,
            table_details=tables_dict[table],
            chunk_size=db_config["chunk_size"],
        )
        # todo make this work!
        # update_data_in_target(
        #     db_config=db_config,
        #     source_db_engine=source_db_engine,
        #     table=table,
        #     table_details=tables_dict[table],
        #     chunk_size=db_config["chunk_size"],
        # )

        completed_tables.append(table)

    if environment == "local":
        update_progress(module_name="load_to_sirius", completed_items=completed_tables)

    if audit == "True":
        log.info(f"Running Post-Audit - Table Copies and Comparisons")
        run_audit(target_db_engine, source_db_engine, "after", log, tables_list)
        log.info(f"Finished Post-Audit - Table Copies and Comparisons")


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
