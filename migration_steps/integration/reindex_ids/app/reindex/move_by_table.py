import logging
import psycopg2

from decorators import timer

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
    query = generate_create_tables_query(db_config, table_list)

    connection_string = db_config["db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
    except Exception as e:
        log.error(e)
        os._exit(1)
    finally:
        cursor.close()
        conn.commit()


def generate_create_tables_query(db_config, table_list):

    create_tables = ""
    for table, details in table_list.items():
        table_name = table

        fks = get_fk_cols_single_table(table=details)

        keys = [x for x in fks + [details["pk"]] if x]
        select_key_cols = [f"{x} as transformation_schema_{x}" for x in keys]

        log.debug(
            f"Generating CREATE TABLE for {db_config['target_schema']}.{table_name} "
            f"with extra cols: {', '.join([f'transformation_schema_{x}' for x in keys])}"
        )

        query = f"""
            CREATE TABLE {db_config['target_schema']}.{table_name}
            AS
                SELECT *,
                    'INSERT' as migration_method,
                    '' as pk_source,
                     {', '.join(select_key_cols)}
                FROM {db_config['source_schema']}.{table_name};
        """

        create_tables += query

    return create_tables
