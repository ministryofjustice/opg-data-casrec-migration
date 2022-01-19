import os
import sys
from pathlib import Path

from rules.deputy_fee_payer import update_deputy_feepayer_id
from rules.backwards_cases_client_link import update_client_id_on_cases
from rules.global_uids import insert_unique_uids
from rules.finance_person_ids import set_finance_person_ids
from rules.client_statuses import update_client_status
from rules.reporting_period_scheduled_events import (
    update_report_log_scheduled_events_foreign_keys,
)
from utilities.clear_tables import clear_tables

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

from quick_validation import check_row_counts

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


config = helpers.get_config(env=environment)


# database
db_config = {
    "db_connection_string": config.get_db_connection_string("migration"),
    "sirius_db_connection_string": config.get_db_connection_string("target"),
    "source_schema": config.schemas["post_transform"],
    "target_schema": config.schemas["integration"],
    "sirius_schema": config.schemas["public"],
    "chunk_size": config.DEFAULT_CHUNK_SIZE,
}
target_db_engine = create_engine(db_config["db_connection_string"])

# logging
log = logging.getLogger("root")
custom_logger.setup_logging(
    env=environment, db_config=db_config, module_name="business rules"
)


@click.command()
@click.option("--correfs", default="")
@click.option(
    "--clear",
    prompt=False,
    default=False,
    help="Clear existing database tables: True or False",
)
def main(clear, correfs):
    allowed_entities = config.allowed_entities(env=os.environ.get("ENVIRONMENT"))
    filtered_correfs = config.get_filtered_correfs(environment, correfs)

    log.info(
        log_title(message="Integration Step: Apply Sirius business rules to Staging DB")
    )
    log.info(
        log_title(
            message=f"Correfs: {', '.join(filtered_correfs) if filtered_correfs else 'all'}"
        )
    )
    log.info(
        log_title(
            message=f"Source: {db_config['source_schema']}, Target: {db_config['target_schema']}, Chunk Size: {db_config['chunk_size']}"
        )
    )
    log.info(log_title(message=f"Enabled entities: {', '.join(allowed_entities)}"))
    log.info(
        log_title(
            message=f"Enabled features: {', '.join(config.enabled_feature_flags(env=os.environ.get('ENVIRONMENT')))}"
        )
    )
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    if clear:
        clear_tables(db_engine=target_db_engine, db_config=db_config)

    insert_unique_uids(db_config=db_config, target_db_engine=target_db_engine)
    update_deputy_feepayer_id(db_config=db_config)
    update_client_id_on_cases(db_config=db_config)
    set_finance_person_ids(db_config=db_config)
    update_report_log_scheduled_events_foreign_keys(db_config=db_config)
    update_client_status(db_config=db_config)

    check_row_counts.count_rows(
        connection_string=db_config["db_connection_string"],
        destination_schema=db_config["target_schema"],
        enabled_entities=allowed_entities,
        correfs=filtered_correfs,
    )


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
