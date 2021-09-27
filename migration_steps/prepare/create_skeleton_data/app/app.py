import sys
import os
from pathlib import Path


current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

from skeleton_data import insert_skeleton_data
import time
import psycopg2
from helpers import get_config
from dotenv import load_dotenv
import helpers
from db_helpers import *
from helpers import *
import logging
import custom_logger
import pprint

pp = pprint.PrettyPrinter(indent=4)

env_path = current_path / "../../../../.env"
shared_path = current_path / "../../../shared"
sql_path = current_path / "../sql"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
config = get_config(environment)


# database
db_config = {
    "db_connection_string": config.get_db_connection_string("migration"),
    "sirius_db_connection_string": config.get_db_connection_string("target"),
    "source_schema": config.schemas["pre_transform"],
    "sirius_schema": config.schemas["public"],
    "chunk_size": config.DEFAULT_CHUNK_SIZE,
}


# logging
log = logging.getLogger("root")
custom_logger.setup_logging(env=environment, module_name="skeleton data")
conn_target = None

skeleton_sqlfile = "skeleton_fixtures.sql"


def main():

    log.info(helpers.log_title(message="Skeleton Fixtures"))
    log.critical(
        "THIS IS A DEVELOPMENT ONLY SCRIPT - IT MUST NEVER RUN ON PRODUCTION DATA"
    )
    log.info("Adding skeleton fixtures\n")
    insert_skeleton_data(db_config=db_config)

    # target_connection = psycopg2.connect(config.get_db_connection_string("target"))
    # execute_sql_file(
    #     sql_path, skeleton_sqlfile, target_connection, config.schemas["public"]
    # )
    # log.info("Finished loading skeleton fixtures\n")


if __name__ == "__main__":
    t = time.process_time()

    log.setLevel(1)
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
