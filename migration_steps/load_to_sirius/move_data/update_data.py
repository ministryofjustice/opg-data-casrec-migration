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


def create_update_statement(schema, table_name, columns, df):

    log.debug(
        f"Updating {len(df)} rows",
        extra={"table_name": table_name, "size": len(df), "action": "insert"},
    )

    if table_name in utilities.SPECIAL_CASES:
        df = utilities.handle_special_cases(table_name=table_name, df=df)

    updates = []
    d = df.to_dict(orient="records")
    for row in d:
        source_id = row["id"]
        del row["id"]
        update_statement = f"UPDATE {schema}.{table_name} SET "

        row = {col: str(data) for col, data in row.items()}
        row = {
            col: utilities.replace_with_sql_friendly_chars_single(val=data)
            for col, data in row.items()
        }

        row = {
            col: f"'{str(data)}'" if str(data) != "" else "NULL"
            for col, data in row.items()
        }

        for i, (col, data) in enumerate(row.items()):
            update_statement += f"{col} = {data}"

            if i + 1 < len(row):
                update_statement += ", "

        update_statement += f" WHERE id = {source_id}"

        updates.append(update_statement)

    return updates


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
    while True:
        try:
            query = f"""
                SELECT {', '.join(columns)}
                FROM {db_config["source_schema"]}.{table_name}
                WHERE method = 'UPDATE'
                ORDER BY {order_by}
                LIMIT {chunk_size} OFFSET {offset};
            """

            log.debug(f"Using source query to get update data: {query}")

            data_to_update = pd.read_sql_query(
                sql=query, con=db_config["source_db_connection_string"]
            )

            log.debug(f"doing offset {offset} for table {table_name}")
            if len(data_to_update) == 0:
                break

            updates = create_update_statement(
                schema=db_config["target_schema"],
                table_name=table_name,
                columns=columns,
                df=data_to_update,
            )

            target_db_engine.execute("; ".join(updates))
            offset += chunk_size
        except Exception as e:
            print(f"e: {e}")
