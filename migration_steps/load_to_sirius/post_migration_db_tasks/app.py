import os
import sys
import threading
from pathlib import Path

from reindex_db import reindex_db
from reset_sequences import reset_all_sequences, reset_all_uid_sequences

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")

import logging.config
import time
import custom_logger
from helpers import log_title
import table_helpers
from dotenv import load_dotenv


# set config
current_path = Path(os.path.dirname(os.path.realpath(__file__)))
env_path = current_path / "../../.env"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
import helpers

config = helpers.get_config(env=environment)


# logging
log = logging.getLogger("root")
custom_logger.setup_logging(env=environment)


# database
db_config = {
    "target_db_connection_string": config.get_db_connection_string("target"),
    "target_schema": config.schemas["public"],
    "target_db_name": os.environ.get("SIRIUS_DB_NAME"),
}


def reset_sequences():
    tables_dict = table_helpers.get_enabled_table_details()
    sequence_list = table_helpers.get_sequences_list(tables_dict)
    reset_all_sequences(sequence_list=sequence_list, db_config=db_config)

    global result
    result = "reset_sequences complete"


def reset_uid_sequences():
    tables_dict = table_helpers.get_enabled_table_details()
    uid_sequence_list = table_helpers.get_uid_sequences_list(tables_dict)
    reset_all_uid_sequences(uid_sequence_list=uid_sequence_list, db_config=db_config)

    global result
    result = "reset_uid_sequences complete"


def reindex():
    reindex_db(db_config=db_config)
    global result
    result = "reindex complete"


def main():
    log.info(log_title(message="Post migration db tasks"))
    log.info(log_title(message=f"Target: {db_config['target_schema']}"))
    log.info(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    jobs = [reset_sequences, reset_uid_sequences, reindex]

    for job in jobs:
        thread = threading.Thread(target=job)
        thread.start()
        thread.join()
        log.debug(f"Result: {result}")


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
