import logging
import sys

import psycopg2

from decorators import timer
import os

log = logging.getLogger("root")


def get_max_pk_from_existing_tables_query(db_schema, table_details):

    max_values_query = ""
    tables_with_pks = {k: v for k, v in table_details.items() if len(v["pk"]) > 0}
    for i, (table, details) in enumerate(tables_with_pks.items()):
        if len(details["pk"]) > 0:
            query = f"""
                SELECT
                    '{table}' as table_name,
                    '{details['pk']}' as column_name,
                    (SELECT max({details['pk']}) from {db_schema}.{table}) as max_value
            """
            if i + 1 < len(tables_with_pks):
                query += " UNION ALL "

            max_values_query += query
    return max_values_query


def get_max_pk_dict(db_connection_string, max_val_query):
    connection_string = db_connection_string
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()
    result_dict = {}

    try:
        cursor.execute(max_val_query)
        max_vals = cursor.fetchall()

        for i in max_vals:
            result_dict[i[0]] = {i[1]: i[2] if i[2] else 0}

    except Exception as e:
        log.debug(e)
        os._exit(1)
    finally:
        cursor.close()
        conn.commit()
    return result_dict


@timer
def update_pks(db_config, table_details):
    max_val_query = get_max_pk_from_existing_tables_query(
        db_schema=db_config["sirius_schema"], table_details=table_details
    )
    max_vals = get_max_pk_dict(
        db_connection_string=db_config["sirius_db_connection_string"],
        max_val_query=max_val_query,
    )

    update_query = ""
    for table, details in table_details.items():
        if len(details["pk"]) > 0:
            pk = details["pk"]
            max_val = max_vals[table][pk]
            log.debug(
                f"Generating UPDATE PK '{pk}' for table '{table}' increasing by {max_val}"
            )

            query = f"""
                UPDATE {db_config['target_schema']}.{table}
                SET {pk} = {pk}+{max_val},
                pk_source = 'reindex_pk'
                WHERE migration_method = 'INSERT';
            """
            update_query += query

    connection_string = db_config["db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    try:
        cursor.execute(update_query)
    except Exception as e:
        log.debug(e)
        os._exit(1)
    finally:
        cursor.close()
        conn.commit()
