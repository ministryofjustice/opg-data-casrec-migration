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
    "source_schema": config.schemas["pre_transform"],
    "target_schema": config.schemas["public"],
    "chunk_size": config.DEFAULT_CHUNK_SIZE,
}
source_db_engine = create_engine(db_config["source_db_connection_string"])
target_db_engine = create_engine(db_config["target_db_connection_string"])

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
    "finance_order",
]


def run_statements_from_file(statement_file):
    sql_statements = []
    sql_statement = ""

    with open(f"{current_path}/sql/{statement_file}.sql", "r") as lines:

        for line in lines:
            if len(line) > 0:
                line = line.replace("{deletions_schema}", config.schemas["deletions"])
                if ";" not in line:
                    sql_statement += f"{line.strip()}\n"
                else:
                    sql_statement += f"{line.strip()}\n"
                    sql_statements.append(sql_statement)
                    sql_statement = ""
    log.info(f"Finished preparing delete statements to run")

    for statement in sql_statements:
        log.info(f"Running statement: \n{statement}")
        with target_db_engine.begin() as connection:
            response = connection.execute(statement)
            log.info(f"{response.rowcount} rows updated\n")


def pre_deletion_flag_alignment_check():
    sql = f"""
         SELECT caserecnumber
         FROM {db_config["target_schema"]}.persons
         WHERE caseactorgroup = 'CLIENT-PILOT-ONE';
    """
    target_response = target_db_engine.execute(sql)
    sirius_cases = [r._mapping["caserecnumber"] for r in target_response]

    sql = f"""
         SELECT "Case" as caserecnumber
         FROM {db_config["source_schema"]}.pat
         WHERE "Sirius" = 'Y';
    """
    source_response = source_db_engine.execute(sql)
    casrec_cases = [r._mapping["caserecnumber"] for r in source_response]

    extra_sirius_flagged_cases = list(set(casrec_cases).difference(sirius_cases))
    extra_cp1_flagged_cases = list(set(sirius_cases).difference(casrec_cases))

    if len(extra_sirius_flagged_cases) > 0 or len(extra_cp1_flagged_cases) > 0:
        if len(extra_sirius_flagged_cases) > 0:
            log.info(
                f"The following cases are marked as migrated on source but aren't CP1 on target: {', '.join(extra_sirius_flagged_cases)}"
            )
        if len(extra_cp1_flagged_cases) > 0:
            log.info(
                f"The following cases are marked as CP1 on target but aren't marked migrated on source: {', '.join(extra_cp1_flagged_cases)}"
            )
        return False
    else:
        log.info("CP1 and Casrec flags align. Continuing...")
        return True


def main():
    log.info(helpers.log_title(message="Delete data adjoining sirius data"))
    log.info(
        helpers.log_title(
            message=f"Source: {db_config['source_schema']}, Target: {db_config['target_schema']}, Chunk Size: {db_config['chunk_size']}"
        )
    )
    log.info(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    if not pre_deletion_flag_alignment_check():
        log.error(
            "There are cases marked with Sirius flag that are not CLIENT-PILOT-ONE"
        )

    if os.environ.get("ENVIRONMENT") in ["preqa", "qa"]:
        # Currently, it takes too long to run event deletions and no amount of indexing or using different joins helps.
        # It's just a huge amount of data in the events table, so we will take the practical approach
        # of just truncating it for our most frequent deploys
        log.info(f"Truncating the events table for speed")
        target_db_engine.execute("TRUNCATE TABLE events;")

    elif os.environ.get("ENVIRONMENT") in ["local", "development"]:
        # Delete finance data linked to clients without a CLIENT-PILOT-ONE flag.
        # This only runs on local and dev environments.
        # Finance data does not get deleted automatically by the deletion script and will fail the build.
        log.info(f"Deleting non-CP1 finance data")
        target_db_engine.execute(
            "DELETE FROM finance_order WHERE id IN (1,2,3,4,5,6,7);"
        )

    run_statements_from_file("deletion_preparation_statements")

    log.info("Checking deletion table counts")
    stop_migration = False
    for table in sirius_deletion_check_tables:
        statement = f"""SELECT id FROM {config.schemas["deletions"]}.{table};"""
        response = target_db_engine.execute(statement)
        row_count = response.rowcount
        log.info(
            f"""Found {row_count} records in {config.schemas["deletions"]}.{table}. Expected 0."""
        )
        if row_count > 0:
            stop_migration = True
            ids = [r._mapping["id"] for r in response]
            log.info("To delete these records manually, run:")
            log.info(
                f"DELETE FROM {table} WHERE id IN ({','.join([str(i) for i in ids])});"
            )

    if stop_migration:
        log.error(
            "Stopping migration due to unexpected deletion counts. Check log output above."
        )
        os._exit(1)

    run_statements_from_file("delete_statements")


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
