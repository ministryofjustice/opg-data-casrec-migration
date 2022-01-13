import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import logging.config
import time
from sqlalchemy import create_engine
import custom_logger
from dotenv import load_dotenv

# set config
env_path = current_path / "../../.env"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
import helpers

config = helpers.get_config(env=environment)


# database
db_config = {
    "source_db_connection_string": config.get_db_connection_string("migration"),
    "target_db_connection_string": config.get_db_connection_string("target"),
    "source_schema": config.schemas["pre_migration"],
    "target_schema": config.schemas["public"],
    "chunk_size": config.DEFAULT_CHUNK_SIZE,
}
source_db_engine = create_engine(db_config["source_db_connection_string"])
target_db_engine = create_engine(config.get_db_connection_string("target"))

# logging
log = logging.getLogger("root")
custom_logger.setup_logging(
    env=environment,
    db_config=db_config,
    module_name="delete data linked to skeleton cases on sirius",
)

completed_tables = []

# Sirius tables that we are not automatically deleting from.
# Stop migration if their respective deletions_ tables are not empty.
sirius_deletion_check_tables = [
    "finance_invoice",
    "finance_ledger",
    "finance_ledger_allocation",
    "finance_remission_exemption",
    "finance_order"
]


def main():
    log.info(helpers.log_title(message="Delete data adjoining sirius data"))
    log.info(
        helpers.log_title(
            message=f"Source: {db_config['source_schema']}, Target: {db_config['target_schema']}, Chunk Size: {db_config['chunk_size']}"
        )
    )
    log.info(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    if os.environ.get("ENVIRONMENT") in ["preproduction", "preqa"]:
        # Currently, it takes too long to run event deletions and no amount of indexing or using different joins helps.
        # It's just a huge amount of data in the events table, so we will take the practical approach
        # of just truncating it for our most frequent deploys (preproduction and preqa)
        log.info(f"Truncating the events table for speed")
        target_db_engine.execute("TRUNCATE TABLE events;")

    sql_statements = []
    sql_statement = ""

    with open(f"{current_path}/sql/delete_statements.sql", "r") as lines:

        for line in lines:
            if len(line) > 0:
                if ";" not in line:
                    sql_statement += f"{line.strip()}\n"
                else:
                    sql_statement += f"{line.strip()}\n"
                    sql_statements.append(sql_statement)
                    sql_statement = ""
    log.info(f"Finished preparing delete statements to run")

    for statement in sql_statements:
        log.info(f"Running statement: \n{statement}")
        response = target_db_engine.execute(statement)
        log.info(f"{response.rowcount} rows updated\n")

    log.info("Checking deletion table counts")
    stop_migration = False
    for table in sirius_deletion_check_tables:
        statement = f"SELECT id FROM deletions.deletions_{table};"
        response = target_db_engine.execute(statement)
        row_count = response.rowcount
        log.info(f"Found {row_count} records in deletions.deletions_{table}. Expected 0.")
        if row_count == 0:
            continue
        stop_migration = True
        ids = [r.values()[0] for r in response]
        log.info("To delete these records manually, run:")
        log.info(f"DELETE FROM {table} WHERE id IN ({','.join([str(i) for i in ids])});")

    if stop_migration:
        log.error("Stopping migration due to unexpected deletion counts. Check log output above.")
        os._exit(1)


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
