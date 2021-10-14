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


def main():
    log.info(helpers.log_title(message="Delete data adjoining sirius data"))
    log.critical(
        "THIS IS A DEVELOPMENT ONLY SCRIPT - IT MUST NOT BE RUN ON PRODUCTION DATA UNTIL FULLY TESTED AND APPROVED!"
    )
    log.info(
        helpers.log_title(
            message=f"Source: {db_config['source_schema']}, Target: {db_config['target_schema']}, Chunk Size: {db_config['chunk_size']}"
        )
    )
    log.info(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

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

    if os.environ.get("ENVIRONMENT") in ["local", "preproduction", "preqa", "qa"]:
        for statement in sql_statements:
            log.info(f"Running statement: \n{statement}")
            response = target_db_engine.execute(statement)
            log.info(f"{response.rowcount} rows updated\n")
    else:
        log.info(f"Not running delete statements {os.environ.get('ENVIRONMENT')}!")


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
