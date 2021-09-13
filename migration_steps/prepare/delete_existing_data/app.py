import os
import sys
from pathlib import Path

from delete_data import get_ids_of_skeleton_persons, delete_data_with_fk_links

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import table_helpers
import logging.config
import time
from sqlalchemy import create_engine
import custom_logger
from dotenv import load_dotenv

# set config
env_path = current_path / "../../.env"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
import helpers

config = helpers.get_config(env=environment)


# database
db_config = {
    "sirius_db_connection_string": config.get_db_connection_string("target"),
}


# logging
log = logging.getLogger("root")
custom_logger.setup_logging(
    env=environment,
    db_config=db_config,
    module_name="delete data linked to skeleton cases on sirius",
)


def main():

    if "delete-skeleton-links" in config.enabled_feature_flags(env=environment):
        log.info(f"Deleting existing skeleton data in Sirius")
        skeleton_person_ids = get_ids_of_skeleton_persons(db_config=db_config)
        log.info(f"Skeleton person_ids: {skeleton_person_ids}")

        if len(skeleton_person_ids) > 0:
            delete_data_with_fk_links(
                db_config=db_config, person_ids=skeleton_person_ids
            )
        else:
            log.debug("No skeleton rows in persons table - not deleting anything")


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
