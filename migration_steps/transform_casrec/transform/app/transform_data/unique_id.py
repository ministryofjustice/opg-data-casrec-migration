import logging
import os

import pandas as pd
import helpers

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


def add_unique_id(
    db_conn_string: str,
    db_schema: str,
    table_definition: dict,
    source_data_df: pd.DataFrame,
) -> pd.DataFrame:

    db_conn = db_conn_string
    db_schema = db_schema
    destination_table_name = table_definition["destination_table_name"]
    unique_column_name = "id"

    query = (
        f"select max({unique_column_name}) from {db_schema}.{destination_table_name};"
    )
    try:
        df = pd.read_sql_query(query, db_conn)
        max_id = df.iloc[0]["max"]
    except Exception:
        max_id = 0

    if max_id is None:
        max_id = 0

    next_id = int(max_id) + 1

    source_data_df.insert(
        0, unique_column_name, range(next_id, next_id + len(source_data_df))
    )

    return source_data_df
