import logging
import os

import psycopg2

from decorators import timer

log = logging.getLogger("root")


@timer
def generate_fk_update_statement_matched_data(db_schema, table_details):

    tables_with_fks = {
        k: v["fks"] for k, v in table_details.items() if len(v["fks"]) > 0
    }
    update_query = ""

    for table, details in tables_with_fks.items():
        for key in details:

            log.debug(
                f"Generating UPDATE FK for {table} using fk {key['column']} and parent field {key['parent_table']}.{key['parent_column']}"
            )
            query = f"""
                UPDATE {db_schema}.{table}
                SET {key['column']} = {key['parent_table']}.{key['parent_column']}
                FROM {db_schema}.{key['parent_table']}
                WHERE cast({table}.{key['column']} as int)
                    = cast({key['parent_table']}.transformation_schema_{key['parent_column']} as int)
                AND {key['parent_table']}.migration_method = 'UPDATE';
            """
            update_query += query
    return update_query


def generate_fk_update_statement_new_data(db_schema, table_details):

    tables_with_fks = {
        k: v["fks"] for k, v in table_details.items() if len(v["fks"]) > 0
    }
    update_query = ""

    for table, details in tables_with_fks.items():
        for key in details:

            log.debug(
                f"Generating UPDATE FK for {table} using fk {key['column']} and parent field {key['parent_table']}.{key['parent_column']}"
            )
            query = f"""
                UPDATE {db_schema}.{table}
                SET {key['column']} = {key['parent_table']}.{key['parent_column']}
                FROM {db_schema}.{key['parent_table']}
                WHERE cast({table}.transformation_schema_{key['column']} as int)
                    = cast({key['parent_table']}.transformation_schema_{key['parent_column']} as int)
                AND {key['parent_table']}.migration_method = 'INSERT';
            """
            update_query += query
    return update_query


@timer
def update_fks(db_config, table_details, match=False):
    if match:
        query = generate_fk_update_statement_matched_data(
            db_schema=db_config["target_schema"], table_details=table_details
        )
    else:
        query = generate_fk_update_statement_new_data(
            db_schema=db_config["target_schema"], table_details=table_details
        )

    # print(f"query: {query}")

    connection_string = db_config["db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
    except Exception as e:
        log.debug(e)
        os._exit(1)
    finally:
        cursor.close()
        conn.commit()
