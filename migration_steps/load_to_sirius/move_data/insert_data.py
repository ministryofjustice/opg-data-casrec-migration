import os
import logging
import sys
from pathlib import Path


import pandas as pd


current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")
import utilities

from helpers import format_error_message
from db_helpers import replace_with_sql_friendly_chars

log = logging.getLogger("root")


def create_insert_statement(schema, table_name, columns, df):

    log.debug(
        f"Inserting {len(df)} rows",
        extra={"table_name": table_name, "size": len(df), "action": "insert"},
    )

    if table_name in utilities.SPECIAL_CASES:
        df = utilities.handle_special_cases(table_name=table_name, df=df)

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


def insert_data_into_target(
    db_config, source_db_engine, target_db_engine, table_name, table_details, chunk_size
):

    log.info(
        f"Inserting new data from {db_config['source_schema']} '{table_name}' table"
    )

    get_cols_query = utilities.get_columns_query(
        table=table_name, schema=db_config["source_schema"]
    )

    columns = [x[0] for x in source_db_engine.execute(get_cols_query).fetchall()]

    columns = utilities.remove_unecessary_columns(columns=columns)

    log.debug(f"columns: {columns}")

    order_by = (
        ", ".join(table_details["order_by"])
        if len(table_details["order_by"]) > 0
        else table_details["pk"]
    )

    log.debug(f"order_by: {order_by}")

    offset = 0
    while True:
        query = f"""
            SELECT {', '.join(columns)}
            FROM {db_config["source_schema"]}.{table_name}
            WHERE migration_method = 'INSERT'
            ORDER BY {order_by}
            LIMIT {chunk_size} OFFSET {offset};;
        """

        log.debug(f"using source query {query}")

        data_to_insert = pd.read_sql_query(
            sql=query, con=db_config["source_db_connection_string"]
        )
        if len(data_to_insert) == 0:
            log.info(f"No data to insert into {table_name}")
            break

        insert_statement = create_insert_statement(
            schema=db_config["target_schema"],
            table_name=table_name,
            columns=columns,
            df=data_to_insert,
        )

        try:
            target_db_engine.execute(insert_statement)
        except Exception as e:
            log.error(
                f"There was an error inserting {len(data_to_insert)} rows "
                f"into {db_config['target_schema']}.{table_name}",
                extra={
                    "table_name": table_name,
                    "size": len(data_to_insert),
                    "action": "insert",
                    "error": format_error_message(e=e),
                },
            )
            os._exit(1)

        offset += chunk_size
        log.debug(f"doing offset {offset} for table {table_name}")
        if len(data_to_insert) < chunk_size:
            break
