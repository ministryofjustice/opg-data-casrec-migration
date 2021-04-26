import json
import os
import sys
from pathlib import Path

from tabulate import tabulate

from checks.address_lines import check_address_line_format
from checks.continuous_ids import check_continuous
from checks.sequences import check_sequences
from checks.uid_sequence import check_uid_sequences
from checks.unique_uids import get_duplicate_uids
from utilities import format_report

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import logging
import time
import click
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
import table_helpers

config = helpers.get_config(env=environment)

# logging
log = logging.getLogger("root")
custom_logger.setup_logging(env=environment, module_name="post migration tests")


# database
db_config = {
    "source_db_connection_string": config.get_db_connection_string("migration"),
    "sirius_db_connection_string": config.get_db_connection_string("target"),
    "source_schema": config.schemas["pre_migration"],
    "sirius_schema": config.schemas["public"],
}
# source_db_engine = create_engine(db_config["source_db_connection_string"])
# target_db_engine = create_engine(db_config["target_db_connection_string"])


@click.command()
def main():

    log.info(log_title(message="Validation Step: check things that are not just data"))

    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    enabled_table_dict = table_helpers.get_enabled_table_details()
    table_list = table_helpers.get_table_list(enabled_table_dict)
    sequence_list = table_helpers.get_sequences_list(enabled_table_dict)
    uid_sequence_list = table_helpers.get_uid_sequences_list(enabled_table_dict)

    tests = []
    sequences = check_sequences(sequences=sequence_list, db_config=db_config)
    tests.append({"name": "Sequences Reset", "result": sequences})
    uid_sequences = check_uid_sequences(
        sequences=uid_sequence_list, db_config=db_config
    )
    tests.append({"name": "UID Sequences Reset", "result": uid_sequences})

    continuous_ids = check_continuous(table_list=table_list, db_config=db_config)
    tests.append({"name": "Continuous IDs", "result": continuous_ids})

    duplicate_uids = get_duplicate_uids(
        uid_sequence_list=uid_sequence_list, db_config=db_config
    )
    tests.append({"name": "Unique UIDs", "result": duplicate_uids})

    # This should be in data validation - once it's added in there remove here pls
    address_line_format = check_address_line_format(db_config=db_config)
    tests.append({"name": "Address Line Formatting", "result": address_line_format})

    report = format_report(tests)

    print(report)


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
