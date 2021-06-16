import os
import sys
from pathlib import Path


current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

from lookups.check_lookups_in_mapping import check_lookups
from lookups.sync_lookups_in_staging import sync_lookups


import logging
import time
from sqlalchemy import create_engine
import custom_logger
from helpers import log_title

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
    "target_schema": config.schemas["pre_migration"],
    "sirius_schema": config.schemas["public"],
    "chunk_size": config.DEFAULT_CHUNK_SIZE,
}
target_db_engine = create_engine(db_config["db_connection_string"])

# logging
log = logging.getLogger("root")
custom_logger.setup_logging(
    env=environment, db_config=db_config, module_name="business rules"
)


def main():
    allowed_entities = config.allowed_entities(env=os.environ.get("ENVIRONMENT"))

    log.info(log_title(message="Integration Step: Syncing Staging DB with Sirius"))
    log.info(
        log_title(
            message=f"Target: {db_config['target_schema']}, Chunk Size: {db_config['chunk_size']}"
        )
    )
    log.info(log_title(message=f"Enabled entities: {', '.join(allowed_entities)}"))
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    # sync_lookups(db_engine=target_db_engine, db_config=db_config)
    check_lookups(db_config=db_config)


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
