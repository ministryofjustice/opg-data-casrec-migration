import os
import sys
from pathlib import Path

# from utilities.progress import update_progress

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

from decorators import files_used
from progress import update_progress
import logging
import time
import click
from sqlalchemy import create_engine
import custom_logger
from helpers import log_title
import helpers
from decorators import timer, mem_tracker

from dotenv import load_dotenv

from entities import (
    clients,
    cases,
    supervision_level,
    deputies,
    bonds,
    death,
    events,
    invoice,
    remarks,
    reporting,
    tasks,
    teams,
    visits,
    warnings,
    crec,
    ledger,
    ledger_allocation,
    fee_reductions,
    timeline,
    finance_order,
    scheduled_events,
)
from utilities.clear_database import clear_tables
from db_insert import InsertData

# set config
current_path = Path(os.path.dirname(os.path.realpath(__file__)))
env_path = current_path / "../../.env"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")


config = helpers.get_config(env=environment)


# database
db_config = {
    "db_connection_string": config.get_db_connection_string("migration"),
    "source_schema": config.schemas["pre_transform"],
    "target_schema": config.schemas["post_transform"],
    "chunk_size": config.DEFAULT_CHUNK_SIZE,
}

# logging
log = logging.getLogger("root")
custom_logger.setup_logging(
    env=environment, db_config=db_config, module_name="transform"
)


allowed_entities = config.allowed_entities(env=os.environ.get("ENVIRONMENT"))

target_db_engine = create_engine(db_config["db_connection_string"])
target_db = InsertData(db_engine=target_db_engine, schema=db_config["target_schema"])


@click.command()
@click.option(
    "--clear",
    prompt=False,
    default=False,
    help="Clear existing database tables: True or False",
)
@click.option("--correfs", default="")
@click.option(
    "--chunk_size",
    prompt=False,
    type=int,
    help="Defaults to 10,000 but can be changed for dev",
    default=db_config["chunk_size"],
)
@mem_tracker
@timer
def main(clear, correfs, chunk_size):
    allowed_entities = config.allowed_entities(env=os.environ.get("ENVIRONMENT"))
    filtered_correfs = config.get_filtered_correfs(environment, correfs)

    log.info(log_title(message="Migration Step: Transform Casrec Data"))
    log.debug(f"Environment: {environment}")
    log.info(f"Correfs: {', '.join(filtered_correfs) if filtered_correfs else 'all'}")
    log.info(f"Enabled entities: {', '.join(allowed_entities)}")
    log.info(
        f"Enabled features: {', '.join(config.enabled_feature_flags(environment))}"
    )
    log.info(f"Source: {db_config['source_schema']}")
    log.info(f"Target: {db_config['target_schema']}")
    log.info(f"Chunk Size: {db_config['chunk_size']}")
    db_config["chunk_size"] = chunk_size if chunk_size else 10000
    log.info(f"Chunking data at {chunk_size} rows")
    version_details = helpers.get_json_version()
    log.info(
        f"Using JSON def version '{version_details['version_id']}' last updated {version_details['last_modified']}"
    )
    log.info(log_title(message="Begin"))

    if clear:
        clear_tables(db_config=db_config)

    cases.runner(target_db=target_db, db_config=db_config)
    deputies.runner(target_db=target_db, db_config=db_config)
    clients.runner(target_db=target_db, db_config=db_config)
    bonds.runner(target_db=target_db, db_config=db_config)
    supervision_level.runner(target_db=target_db, db_config=db_config)
    death.runner(target_db=target_db, db_config=db_config)
    events.runner(target_db=target_db, db_config=db_config)
    invoice.runner(target_db=target_db, db_config=db_config)
    remarks.runner(target_db=target_db, db_config=db_config)
    reporting.runner(target_db=target_db, db_config=db_config)
    tasks.runner(target_db=target_db, db_config=db_config)
    teams.runner(target_db=target_db, db_config=db_config)
    visits.runner(target_db=target_db, db_config=db_config)
    warnings.runner(target_db=target_db, db_config=db_config)
    crec.runner(target_db=target_db, db_config=db_config)
    ledger.runner(target_db=target_db, db_config=db_config)
    ledger_allocation.runner(target_db=target_db, db_config=db_config)
    fee_reductions.runner(target_db=target_db, db_config=db_config)
    timeline.runner(target_db=target_db, db_config=db_config)
    finance_order.runner(target_db=target_db, db_config=db_config)
    scheduled_events.runner(target_db=target_db, db_config=db_config)

    update_progress(module_name="transform", completed_items=files_used)


if __name__ == "__main__":
    t = time.process_time()

    try:
        main()
    except Exception as e:
        if environment in ['local', 'dev']:
            log.exception(e)
        else:
            err_str = f"Unexpected error: {type(e).__name__}. Stack trace:"
            tb = e.__traceback__
            while tb is not None:
                err_str += "\n\t" + f"File: {tb.tb_frame.f_code.co_filename}; Line: {tb.tb_lineno}"
                tb = tb.tb_next
            log.error(err_str)
        os._exit(1)

    print(f"Total time: {round(time.process_time() - t, 2)}")
