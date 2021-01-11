import sys
import os
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import time
import psycopg2
from helpers import get_config
from dotenv import load_dotenv
from helpers import log_title
from db_helpers import *
from entities import client
from entities import address
import logging
import custom_logger
import click

sql_path = current_path / "sql"
env_path = current_path / "../../../../.env"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
config = get_config(environment)

# logging
custom_logger.custom_log_level(levels=config.custom_log_levels)
verbosity_levels = config.verbosity_levels
log = logging.getLogger("root")
log.addHandler(custom_logger.MyHandler())


def set_logging_level(verbose):
    try:
        log.setLevel(verbosity_levels[verbose])
    except KeyError:
        log.setLevel("INFO")
        log.info(f"{verbose} is not a valid verbosity level")


@click.command()
@click.option("-v", "--verbose", count=True)
def main(verbose):
    set_logging_level(verbose)
    log.info(log_title(message="Merge Target IDs"))

    conn_migration = psycopg2.connect(config.get_db_connection_string("migration"))
    conn_target = psycopg2.connect(config.get_db_connection_string("target"))

    log.info("Fetch matching IDs from target (Sirius)")
    log.info("- Clients")
    client.fetch_target_ids(config, conn_migration, conn_target)
    log.info("- Addresses")
    address.fetch_target_ids(config, conn_migration, conn_target)

    log.info("Merge target IDs in with integration data")
    log.info("- Clients")
    client.merge_target_ids(config, conn_migration, conn_target)
    log.info("- Addresses")
    address.merge_target_ids(config, conn_migration, conn_target)


if __name__ == "__main__":
    t = time.process_time()

    log.setLevel(1)
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    if environment in ("local", "development"):
        main()
    else:
        log.warning("Skipping step not designed to run on environment %s", environment)

    print(f"Total time: {round(time.process_time() - t, 2)}")
