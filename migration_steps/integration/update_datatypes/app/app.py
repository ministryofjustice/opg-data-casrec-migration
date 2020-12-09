import time

import sys
import os
from pathlib import Path


current_path = Path(os.path.dirname(os.path.realpath(__file__)))

sys.path.insert(0, str(current_path) + "/../../../shared")


import logging
import click
import custom_logger
from helpers import log_title
import helpers
from dotenv import load_dotenv
from config2 import get_config
from entities.clients import update_client_data_types

# set config
current_path = Path(os.path.dirname(os.path.realpath(__file__)))
env_path = current_path / "../../.env"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
config = get_config(environment)

# logging
log = logging.getLogger("root")
log.addHandler(custom_logger.MyHandler())

config.custom_log_level()


@click.command()
@click.option("-v", "--verbose", count=True)
def main(verbose):
    config.set_logging_level(verbose=verbose)

    log.info(log_title(message="Migration Step: Update Datatypes"))
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    source_schema = config.schemas["post_transform"]
    target_schema = config.schemas["integration"]

    update_client_data_types(
        config=config, source_schema=source_schema, target_schema=target_schema
    )


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
