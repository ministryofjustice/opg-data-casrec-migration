import json
import os
import logging
import sys
from pathlib import Path

import numpy as np
import psycopg2
from psycopg2 import errors
import pandas as pd


current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")

from helpers import format_error_message
import db_helpers


log = logging.getLogger("root")


def update_data_in_target(
    db_config, source_db_engine, table, table_details, chunk_size
):
    print("UPDATING")

    # log.info(
    #     f"Updating existing data from {db_config['source_schema']} '{table}' table"
    # )
    # get_cols_query = get_columns_query(table=table, schema=db_config["source_schema"])
    #
    # columns = [x[0] for x in source_db_engine.execute(get_cols_query).fetchall()]
    #
    # columns = remove_unecessary_columns(columns=columns)
    # order_by = (
    #     ", ".join(table_details["order_by"])
    #     if len(table_details["order_by"]) > 0
    #     else table_details["pk"]
    # )
    #
    # offset = 0
    # while True:
    #     query = f"""
    #         SELECT {', '.join(columns)} FROM {db_config["source_schema"]}.{table}
    #         WHERE method = 'UPDATE'
    #         ORDER BY {order_by}
    #         LIMIT {chunk_size} OFFSET {offset};
    #     """
    #
    #     data_to_update = pd.read_sql_query(
    #         sql=query, con=db_config["source_db_connection_string"]
    #     )
    #
    #     if table in SPECIAL_CASES:
    #         data_to_update = handle_special_cases(table_name=table, df=data_to_update)
    #
    #     for col in columns:
    #         data_to_update[col] = (
    #             data_to_update[col]
    #             .astype(str)
    #             .replace({"NaT": None, "None": None, "NaN": None})
    #         )
    #
    #     log.debug(f"Updating {len(data_to_update)} rows")
    #
    #     keepalive_kwargs = {
    #         "keepalives": 1,
    #         "keepalives_idle": 30,
    #         "keepalives_interval": 5,
    #         "keepalives_count": 5,
    #     }
    #     target_connection = psycopg2.connect(
    #         db_config["target_db_connection_string"], **keepalive_kwargs
    #     )
    #     db_helpers.execute_update(
    #         conn=target_connection, df=data_to_update, table=table, pk_col="id"
    #     )
    #
    #     offset += chunk_size
    #     log.debug(f"doing offset for update: {offset} for table {table}")
    #     if len(data_to_update) < chunk_size:
    #         break
