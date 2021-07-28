import json
import os
import logging
import sys
from pathlib import Path

import numpy as np
import psycopg2
from psycopg2 import errors
import pandas as pd

import utilities

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")

from helpers import format_error_message
import db_helpers


log = logging.getLogger("root")


def update_data_in_target(
    db_config, source_db_engine, target_db_engine, table_name, table_details, chunk_size
):

    log.info(
        f"Updating existing data from {db_config['source_schema']} '{table_name}' table"
    )

    get_cols_query = utilities.get_columns_query(
        table=table_name, schema=db_config["source_schema"]
    )

    columns = [x[0] for x in source_db_engine.execute(get_cols_query).fetchall()]

    columns = utilities.remove_unecessary_columns(
        columns=columns,
        cols_to_keep=table_details["existing_data"]["keep_original_data"],
    )

    order_by = (
        ", ".join(table_details["order_by"])
        if len(table_details["order_by"]) > 0
        else table_details["pk"]
    )

    offset = 0
    query = f"""
        SELECT {', '.join(columns)}
        FROM {db_config["source_schema"]}.{table_name}
        WHERE method = 'UPDATE'
        ORDER BY {order_by}
        LIMIT {chunk_size} OFFSET {offset};
    """

    log.debug(f"Using source query to get update data: {query}")

    data_to_insert = pd.read_sql_query(
        sql=query, con=db_config["source_db_connection_string"]
    )
    if table_name in utilities.SPECIAL_CASES:
        data_to_insert = utilities.handle_special_cases(
            table_name=table_name, df=data_to_insert
        )

    connection_string = db_config["target_db_connection_string"]
    conn = psycopg2.connect(connection_string)

    db_helpers.execute_update(
        conn=conn, df=data_to_insert, table=table_name, pk_col="id"
    )
