"""
Insert/update data in the casrec db. The purpose of this is to enable
testing of data which needs to change over time. For example, the relationship
between a casrec account End Date and the current date affects the
status and reviewstatus of the target record in the annual_report_logs table.
"Fixed" fixture data with a static date in the End Date field is not able
to recreate the various End Dates required to test all of the possible
output status and reviewstatus target values.

This script should run before the transform step begins, so that the fixtures
added are part of the source data for the transformation.
"""

import logging
import os
import pandas as pd
import sys
from sqlalchemy import create_engine
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

from account_fixtures import ACCOUNT_FIXTURES
import custom_logger
from helpers import get_config, log_title


LOG = logging.getLogger("root")
LOG.setLevel("INFO")
LOG.addHandler(custom_logger.MyHandler())

CONFIG = get_config(os.environ.get("ENVIRONMENT"))

SCHEMA = CONFIG.schemas["pre_transform"]

ALL_FIXTURES = ACCOUNT_FIXTURES


# field_and_value is a tuple (field, value,)
# create a "field" = 'value' sub clause
def _format_sub_clause(field_and_value):
    # set to empty string as casrec doesn't have nulls,
    # only empty strings
    field, value = field_and_value

    if value is None:
        value = ""

    return f"\"{field}\" = '{value}'"


if __name__ == "__main__":
    LOG.info(log_title(message="DYNAMIC FIXTURES"))
    LOG.info(f"Loading dynamic fixtures into schema {SCHEMA}")
    # set up db conn
    db_conn_string = CONFIG.get_db_connection_string("migration")
    engine = create_engine(db_conn_string)

    # add the fixtures to the db
    for fixture in ALL_FIXTURES:
        for update in fixture["updates"]:
            params = update["source_criteria"]
            params["schema"] = SCHEMA

            select_sql = fixture["source_query"].format(**params)
            df = pd.read_sql(select_sql, engine)

            # make the update SQL for each row in the dataframe and execute it
            for _, row in df.iterrows():
                set_values = map(_format_sub_clause, update["set"].items())

                where = map(
                    lambda column: _format_sub_clause(
                        (
                            column,
                            row[column],
                        )
                    ),
                    df.columns,
                )

                update_sql = fixture["update_query"].format(
                    set_clause=", ".join(set_values),
                    where_clause=" AND ".join(where),
                    schema=SCHEMA,
                )

                LOG.info(f"Running update SQL: {update_sql}")

                engine.execute(update_sql)
