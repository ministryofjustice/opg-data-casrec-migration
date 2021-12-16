import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import time
import psycopg2

from dotenv import load_dotenv
from helpers import log_title, get_config
from db_helpers import *
import logging
import custom_logger
import click

env_path = current_path / "../../../../.env"
sql_path = current_path / "sql"
shared_sql_path = current_path / "../../../shared/sql"
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
@click.option("-i", "--preserve_schemas", default="reference")
def main(verbose, preserve_schemas):
    set_logging_level(verbose)
    conn_source = psycopg2.connect(config.get_db_connection_string("migration"))
    log.info("Dropping schemas on Source")
    delete_all_schemas(log=log, conn=conn_source, preserve_schemas=preserve_schemas)
    conn_source.close()


if __name__ == "__main__":
    t = time.process_time()

    log.setLevel(1)
    log.info(log_title(message="Initialise Environments"))
    log.debug(f"Initialise Source (Environment: {os.environ.get('ENVIRONMENT')})")

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
