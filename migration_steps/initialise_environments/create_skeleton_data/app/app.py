import sys
import os
from pathlib import Path

from sqlalchemy import create_engine


current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

from lookups.check_lookups_in_mapping import check_lookups
from lookups.sync_lookups_in_staging import sync_lookups
from lookups.dev_data_fixes import (
    amend_dev_data,
    amend_blank_correfs,
    amend_blank_away_dates,
)

from skeleton_data import insert_skeleton_data
import time
from helpers import get_config
from dotenv import load_dotenv
import helpers
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
    "target_schema": config.schemas["pre_migration"],
    "sirius_schema": config.schemas["public"],
    "chunk_size": config.DEFAULT_CHUNK_SIZE,
}
casrec_db_engine = create_engine(db_config["db_connection_string"])
sirius_db_engine = create_engine(db_config["sirius_db_connection_string"])

# logging
log = logging.getLogger("root")
custom_logger.setup_logging(env=environment, module_name="skeleton data")
conn_target = None


def main():

    log.info(helpers.log_title(message="Skeleton Fixtures"))
    log.critical(
        "THIS IS A DEVELOPMENT ONLY SCRIPT - IT MUST NEVER RUN ON PRODUCTION DATA"
    )
    log.info("Adding skeleton fixtures\n")
    insert_skeleton_data(db_config=db_config)

    amend_dev_data(db_engine=sirius_db_engine)
    amend_blank_correfs(db_engine=casrec_db_engine)
    if config.migration_phase["migration_identifier"] == "CASRECMIGRATION_P3":
        amend_blank_away_dates(db_engine=casrec_db_engine)
    check_lookups(db_config=db_config)
    sync_lookups(db_engine=casrec_db_engine, db_config=db_config)


if __name__ == "__main__":
    t = time.process_time()

    log.setLevel(1)
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
