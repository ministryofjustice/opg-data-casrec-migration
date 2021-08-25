import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import time
import psycopg2
from config import get_config
from dotenv import load_dotenv
from helpers import log_title
from db_helpers import *
import logging
import custom_logger
import click

env_path = current_path / "../../../../.env"
sql_path = current_path / "sql"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
config = get_config(environment)
lay_team = config.lay_team_filter(env=environment)

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
@click.option("--team", default="")
@click.option("--clear", prompt=False, default=False)
def main(verbose, team, clear):
    set_logging_level(verbose)
    log.info(log_title(message="Filter Data"))
    conn_source = psycopg2.connect(config.get_db_connection_string("migration"))

    if team:
        if lay_team:
            log.info(f"Lay Team filtering specified in param store: Team {lay_team}")
            log.info(f"Overriding with Lay Team requested at runtime: Team {team}")
        else:
            log.info(f"Lay Team filtering requested at runtime: Team {team}")
    elif lay_team:
        team = lay_team
        log.info(f"Lay Team filtering specified in param store: Team {team}")
    else:
        log.info(f"No filtering requested, proceed with migrating ALL.")

    if team:
        team = "T" + team
        log.info(f"Deleting data not associated with {team}")
        execute_generated_sql(
            sql_path,
            "delete_filtered_source_data.template.sql",
            "{team}",
            team,
            conn_source,
        )


if __name__ == "__main__":
    t = time.process_time()

    log.setLevel(1)
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
