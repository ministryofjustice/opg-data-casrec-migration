import os
import sys
import threading
from pathlib import Path

from finance_batch_numbers import set_all_batch_numbers
from finance_person_ids import set_all_finance_person_ids
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


# database
db_config = {
    "source_schema": config.schemas["public"],
    "target_db_connection_string": config.get_db_connection_string("target"),
    "target_schema": config.schemas["public"],
    "target_db_name": os.environ.get("SIRIUS_DB_NAME"),
}

# logging
log = logging.getLogger("root")
custom_logger.setup_logging(
    env=environment, db_config=db_config, module_name="post migration db tasks"
)


def reset_sequences():
    log.info("Starting reset_sequences")
    tables_dict = table_helpers.get_enabled_table_details()
    sequence_list = table_helpers.get_sequences_list(tables_dict)
    reset_all_sequences(sequence_list=sequence_list, db_config=db_config)

    global result
    result = "reset_sequences complete"


def reset_uid_sequences():
    log.info("Starting reset_uid_sequences")
    tables_dict = table_helpers.get_enabled_table_details()
    uid_sequence_list = table_helpers.get_uid_sequences_list(tables_dict)
    reset_all_uid_sequences(uid_sequence_list=uid_sequence_list, db_config=db_config)

    global result
    result = "reset_uid_sequences complete"


def reindex():
    log.info("Starting reindex")
    reindex_db(db_config=db_config)
    global result
    result = "reindex complete"


def set_finance_person_ids():
    log.info("Starting set_finance_person_ids")
    set_all_finance_person_ids(db_config=db_config)
    global result
    result = "set_finance_person_ids complete"


def set_batch_numbers():
    log.info("Starting set_batch_numbers")
    set_all_batch_numbers(db_config=db_config)
    global result
    result = "set_batch_numbers complete"


def main():
    log.info(log_title(message="Post migration db tasks"))
    log.info(log_title(message=f"Target: {db_config['target_schema']}"))
    log.info(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    # feature_flag load-to-sirius
    if "load-to-sirius" not in config.enabled_feature_flags(env=environment):
        return False

    jobs = [
        reset_sequences,
        reset_uid_sequences,
        set_finance_person_ids,
        set_batch_numbers,
    ]

    for job in jobs:
        thread = threading.Thread(target=job)
        thread.start()
        thread.join()
        log.debug(f"Result: {result}")


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
