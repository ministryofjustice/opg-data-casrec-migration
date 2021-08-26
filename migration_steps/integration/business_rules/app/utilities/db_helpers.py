import logging
import sys
from pathlib import Path

import psycopg2
import os

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../../shared")

from decorators import timer

log = logging.getLogger("root")


def generate_select_query(schema, table, columns=None, where_clause=None):
    if columns:
        query = f"SELECT {', '.join(columns)} from {schema}.{table}"
    else:
        query = f"SELECT * from {schema}.{table}"

    if where_clause:
        where = ""
        for i, (item, value) in enumerate(where_clause.items()):
            if i == 0:
                where += " WHERE "
            else:
                where += " AND "

            where += f"{item} = '{value}'"

        query += where

    query += ";"

    return query


def get_max_id_from_existing_table(db_connection_string, db_schema, table, id="id"):
    connection_string = db_connection_string
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    query = f"SELECT max({id}) from {db_schema}.{table};"
    max_id = 0

    try:
        cursor.execute(query)
        max_id = cursor.fetchall()[0][0]
        if max_id:
            log.debug(f"Max '{id}' in table '{db_schema}.{table}': {max_id}")
        else:
            log.debug(
                f"No data for '{id}' in table '{db_schema}.{table}', setting max_id to 0"
            )

    except psycopg2.DatabaseError:
        log.debug(
            f"Database error for '{id}' in table '{db_schema}.{table}', setting max_id to 0"
        )
    except (Exception) as error:
        log.error("Error: %s" % error)
    finally:
        cursor.close()
        return max_id


@timer
def update_ids(db_connection_string, db_schema, table, column_name, update_data):
    connection_string = db_connection_string
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    log.info(f'Updating {table}."{column_name}" IDs...')

    try:
        cursor.execute(
            f"""
            CREATE TEMP TABLE temp_ids(id bigint, "{column_name}" bigint) ON COMMIT DROP ;
        """
        )

        insert_query = f"""
            INSERT INTO temp_ids VALUES
        """
        update_data_list = list(update_data)
        for i, (id, update_id) in enumerate(update_data_list):
            insert_query += f"({id}, {update_id})"
            if i + 1 < len(update_data_list):
                insert_query += ", "
            else:
                insert_query += ";"

        cursor.execute(insert_query)

        cursor.execute(
            f"""
            UPDATE {db_schema}.{table}
            SET "{column_name}" = temp_ids."{column_name}"
            FROM temp_ids
            WHERE temp_ids.id = {table}.id
        """
        )
    except (Exception) as error:
        log.error("Error: %s" % error)
    finally:
        row_count = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
    log.info(f"rows affected: {row_count}")
    return row_count
