import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import logging.config
import time
import psycopg2
import custom_logger
from dotenv import load_dotenv
import click
import helpers
from db_helpers import execute_sql_file
from helpers import log_title

env_path = current_path / "../../.env"
load_dotenv(dotenv_path=env_path)
environment = os.environ.get("ENVIRONMENT")
config = helpers.get_config(env=environment)

custom_logger.setup_logging(
    env=environment,
    module_name="count pre-existing client-pilot-one data on sirius",
)
log = logging.getLogger("root")
config.custom_log_level()

@click.command()
@click.option("--correfs", default="")
def main(correfs):
    allowed_entities = config.allowed_entities(env=environment)
    filtered_correfs = config.get_filtered_correfs(environment, correfs)

    log.info(log_title(message="Migration Step: Count Existing Client Pilot One data on target"))
    log.debug(f"Environment: {environment}")
    log.info(f"Correfs: {', '.join(filtered_correfs) if filtered_correfs else 'all'}")
    log.info(f"Enabled entities: {', '.join(allowed_entities)}")
    log.info(
        f"Enabled features: {', '.join(config.enabled_feature_flags(environment))}"
    )
    log.info(log_title(message="Begin"))
    conn_target = psycopg2.connect(config.get_db_connection_string("target"))
    execute_sql_file(current_path / "sql", "count_existing_pc1.sql", conn_target)
    log.info(f"Updated count record with pre-existing Client Pilot One counts from Sirius.")


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
