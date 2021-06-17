import logging
import psycopg2

from decorators import timer
from helpers import format_error_message

from table_helpers import get_fk_cols_single_table
import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../../../shared")

log = logging.getLogger("root")


def create_schema(target_db_connection, schema_name):
    statement = f"""
        CREATE SCHEMA IF NOT EXISTS {schema_name};
    """

    connection_string = target_db_connection
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    try:
        cursor.execute(statement)
    except Exception as e:
        log.error(e)
        os._exit(1)
    finally:
        cursor.close()
        conn.commit()


@timer
def move_all_tables(db_config, table_list):
    for table, details in table_list.items():

        query = generate_create_single_table_query(
            db_config=db_config, table_name=table, table_details=details
        )

        connection_string = db_config["db_connection_string"]
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()

        try:
            cursor.execute(query)
        except psycopg2.DatabaseError as e:
            log.error(
                f"error moving data from {db_config['source_schema']} to {db_config['target_schema']} schema - table probably doesn't exist",
                extra={"error": format_error_message(e=e)},
            )
        except Exception as e:
            log.error(e, extra={"error": format_error_message(e=e)})
            os._exit(1)
        finally:
            cursor.close()
            conn.commit()


def generate_create_single_table_query(db_config, table_name, table_details):

    fks = get_fk_cols_single_table(table=table_details)

    keys = [x for x in fks + [table_details["pk"]] if x]
    select_key_cols = [f"{x} as transformation_schema_{x}" for x in keys]

    log.debug(
        f"Generating CREATE TABLE for {db_config['target_schema']}.{table_name} "
        f"with extra cols: {', '.join([f'transformation_schema_{x}' for x in keys])}"
    )

    query = f"""
        CREATE TABLE {db_config['target_schema']}.{table_name}
        AS
            SELECT *,
                null as method,
                 {', '.join(select_key_cols)}
            FROM {db_config['source_schema']}.{table_name};
    """

    return query
