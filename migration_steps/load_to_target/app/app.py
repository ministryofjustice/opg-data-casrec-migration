import os
import time
import psycopg2
import get_shared_utilities
from config_jack import get_config
from pathlib import Path
from dotenv import load_dotenv
from helpers import log_title
from db_helpers import *
from entities import client
from entities import address
import logging
import custom_logger
import click

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sql_path = current_path / 'sql'
env_path = current_path / "../.env"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
config = get_config(environment)

# logging
log = logging.getLogger("root")
log.addHandler(custom_logger.MyHandler())
config.custom_log_level()
verbosity_levels = config.verbosity_levels

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
    log.info(log_title(message="Migration Step: Load To Target (do migration)"))

    conn_migration = psycopg2.connect(config.get_db_connection_string("migration"))
    conn_target = psycopg2.connect(config.get_db_connection_string("target"))

    log.info("Migrate: Update skeleton data on target")
    log.info("- Clients")
    client.target_update(config, conn_migration, conn_target)
    log.info("- Addresses")
    address.target_update(config, conn_migration, conn_target)

    log.info("Migrate: Insert new data to target")
    log.info("- Clients")
    client.target_add(config, conn_migration, conn_target)

    log.info("- - Re-index newly added clients")
    client.reindex_target_ids(config, conn_migration, conn_target)
    address.reindex_target_ids(config, conn_migration)

    log.info("- Addresses")
    address.target_add(config, conn_migration, conn_target)

    log.critical(log_title(message="Migration complete."))


if __name__ == "__main__":
    t = time.process_time()

    log.setLevel(1)
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    if environment in ("local", "development"):
        main()
    else:
        log.warning("Skipping step not designed to run on environment %s", environment)

    print(f"Total time: {round(time.process_time() - t, 2)}")
