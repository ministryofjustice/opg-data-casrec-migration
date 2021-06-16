import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

from lookups.check_lookups_in_mapping import check_lookups
from lookups.sync_lookups_in_staging import sync_lookups


import time
from config import get_config
from dotenv import load_dotenv
from db_helpers import *
import logging
import custom_logger


env_path = current_path / "../../../../.env"
shared_sql_path = current_path / "../../../shared/sql"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
config = get_config(environment)


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

    log.info("Take a fresh copy of the Sirius data structure")
    copy_schema(
        log=log,
        sql_path=shared_sql_path,
        from_config=config.db_config["target"],
        from_schema=config.schemas["public"],
        to_config=config.db_config["migration"],
        to_schema=config.schemas["pre_migration"],
        structure_only=True,
    )

    check_lookups(db_config=db_config)
    sync_lookups(db_engine=target_db_engine, db_config=db_config)


if __name__ == "__main__":
    t = time.process_time()

    log.setLevel(1)
    log.debug(f"create_stage_schema (Environment: {os.environ.get('ENVIRONMENT')})")

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
