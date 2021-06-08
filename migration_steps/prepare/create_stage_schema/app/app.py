import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import time
from config import get_config
from dotenv import load_dotenv
from db_helpers import *
import logging
import custom_logger
import click

env_path = current_path / "../../../../.env"
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
def main(verbose):
    set_logging_level(verbose)

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


if __name__ == "__main__":
    t = time.process_time()

    log.setLevel(1)
    log.debug(f"create_stage_schema (Environment: {os.environ.get('ENVIRONMENT')})")

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
