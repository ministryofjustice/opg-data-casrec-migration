import sys
import os
import time
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

from helpers import get_config, log_title
from dotenv import load_dotenv
from db_helpers import copy_schema
import logging
import custom_logger

env_path = current_path / "../../../../.env"
shared_path = current_path / "../../../shared"
sql_path = shared_path / "sql"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
config = get_config(environment)

# logging
log = logging.getLogger("root")
custom_logger.setup_logging(env=environment, module_name="prepare")


def copy_casrec_schema():
    copy_schema(
        log=log,
        sql_path=sql_path,
        from_config=config.db_config["casrec"],
        from_schema=config.schemas["pre_transform"],
        to_config=config.db_config["migration"],
        to_schema=config.schemas["pre_transform"],
    )


def main():
    log.info(log_title(message="Migration Step: Copy Schema To CasRec"))
    log.debug(f"Environment: {environment}")
    copy_casrec_schema()


if __name__ == "__main__":
    t = time.process_time()

    log.setLevel(1)
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
