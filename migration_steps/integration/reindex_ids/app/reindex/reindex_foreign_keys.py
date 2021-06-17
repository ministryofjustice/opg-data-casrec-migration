import logging
import os

import psycopg2

from decorators import timer
from helpers import format_error_message

log = logging.getLogger("root")


@timer
def generate_single_fk_update_statement(db_schema, table_name, table_details):

    for key in table_details:
        log.debug(f"Generating UPDATE FK for {table_name} using fk {key['column']}")
        query = f"""
            UPDATE {db_schema}.{table_name}
            SET {key['column']} = {key['parent_table']}.{key['parent_column']}
            FROM {db_schema}.{key['parent_table']}
            WHERE cast({table_name}.transformation_schema_{key['column']} as int)
                = cast({key['parent_table']}.transformation_schema_{key['parent_column']} as int)
            AND {table_name}.method = 'INSERT';
        """
    return query


@timer
def update_fks(db_config, table_details):

    tables_with_fks = {
        k: v["fks"] for k, v in table_details.items() if len(v["fks"]) > 0
    }
    for table, details in tables_with_fks.items():

        query = generate_single_fk_update_statement(
            db_schema=db_config["target_schema"],
            table_name=table,
            table_details=details,
        )

        connection_string = db_config["db_connection_string"]
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()

        try:
            cursor.execute(query)
        except psycopg2.DatabaseError as e:
            log.error(
                f"error reindexing FK for table {table}- table probably doesn't exist",
                extra={"error": format_error_message(e=e)},
            )
        except Exception as e:
            log.debug(e, extra={"error": format_error_message(e=e)})
            os._exit(1)
        finally:
            cursor.close()
            conn.commit()
