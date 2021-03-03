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

import db_helpers

completed_tables = []

log = logging.getLogger("root")

SPECIAL_CASES = ["addresses"]


def handle_special_cases(table_name, df):
    if table_name == "addresses":
        log.debug("Reformatting 'address_lines' to json")
        df["address_lines"] = df["address_lines"].apply(json.dumps)
    return df


def replace_with_sql_friendly_chars(row_as_list):
    row = [
        str(
            x.replace("'", "''")
            .replace("NaT", "")
            .replace("nan", "")
            .replace("None", "")
            .replace("&", "and")
            .replace(";", "-")
            .replace("%", "percent")
        )
        for x in row_as_list
    ]

    return row


def get_columns_query(table, schema):
    return f"""
        SELECT column_name FROM information_schema.columns
        WHERE table_schema = '{schema}'
        AND table_name = '{table}';
        """


def remove_unecessary_columns(columns):
    unecessary_field_names = ["method"]

    return [column for column in columns if column not in unecessary_field_names]


def create_insert_statement(schema, table_name, columns, df):

    if table_name in SPECIAL_CASES:
        df = handle_special_cases(table_name=table_name, df=df)

    insert_statement = f'INSERT INTO "{schema}"."{table_name}" ('
    for i, col in enumerate(columns):
        insert_statement += f'"{col}"'
        if i + 1 < len(columns):
            insert_statement += ","

    insert_statement += ") \n VALUES \n"

    for i, row in enumerate(df.values.tolist()):

        row = [str(x) for x in row]
        row = replace_with_sql_friendly_chars(row_as_list=row)
        row = [f"'{str(x)}'" if str(x) != "" else "NULL" for x in row]

        single_row = ", ".join(row)

        insert_statement += f"({single_row})"

        if i + 1 < len(df):
            insert_statement += ",\n"
        else:
            insert_statement += ";\n\n\n"
    return insert_statement


def insert_data_into_target(db_config, source_db_engine, target_db_engine, table, pk):

    log.info(f"Inserting new data from {db_config['source_schema']} '{table}' table")
    get_cols_query = get_columns_query(table=table, schema=db_config["source_schema"])

    columns = [x[0] for x in source_db_engine.execute(get_cols_query).fetchall()]

    columns = remove_unecessary_columns(columns=columns)

    chunk_size = 10000
    offset = 0
    while True:
        query = f"""
            SELECT {', '.join(columns)}
            FROM {db_config["source_schema"]}.{table}
            WHERE method = 'INSERT'
            ORDER BY {pk}
            LIMIT {chunk_size} OFFSET {offset};;
        """

        data_to_insert = pd.read_sql_query(
            sql=query, con=db_config["source_db_connection_string"]
        )

        insert_statement = create_insert_statement(
            schema=db_config["target_schema"],
            table_name=table,
            columns=columns,
            df=data_to_insert,
        )

        log.debug(f"Inserting {len(data_to_insert)} rows")

        try:
            target_db_engine.execute(insert_statement)
        except Exception as e:
            log.error(e)

        offset += chunk_size
        log.debug(f"doing offset {offset} for table {table}")
        if len(data_to_insert) < chunk_size:
            break


def update_data_in_target(db_config, source_db_engine, table, pk):

    log.info(
        f"Updating existing data from {db_config['source_schema']} '{table}' table"
    )
    get_cols_query = get_columns_query(table=table, schema=db_config["source_schema"])

    columns = [x[0] for x in source_db_engine.execute(get_cols_query).fetchall()]

    columns = remove_unecessary_columns(columns=columns)

    chunk_size = 10000
    offset = 0
    while True:
        query = f"""
            SELECT {', '.join(columns)} FROM {db_config["source_schema"]}.{table}
            WHERE method = 'UPDATE'
            ORDER BY {pk}
            LIMIT {chunk_size} OFFSET {offset};
        """

        data_to_update = pd.read_sql_query(
            sql=query, con=db_config["source_db_connection_string"]
        )

        if table in SPECIAL_CASES:
            data_to_update = handle_special_cases(table_name=table, df=data_to_update)

        for col in columns:
            data_to_update[col] = (
                data_to_update[col]
                .astype(str)
                .replace({"NaT": None, "None": None, "NaN": None})
            )

        log.debug(f"Updating {len(data_to_update)} rows")

        target_connection = psycopg2.connect(db_config["target_db_connection_string"])
        db_helpers.execute_update(
            conn=target_connection, df=data_to_update, table=table, pk_col="id"
        )

        offset += chunk_size
        log.debug(f"doing offset for update: {offset} for table {table}")
        if len(data_to_update) < chunk_size:
            break
