import logging
import os

import psycopg2

from decorators import timer

log = logging.getLogger("root")


@timer
def generate_fk_update_statement(db_schema, table_details, match):

    tables_with_fks = {
        k: v["fks"] for k, v in table_details.items() if len(v["fks"]) > 0
    }
    update_query = ""

    for table, details in tables_with_fks.items():
        for key in details:

            if match:
                method = "UPDATE"
            else:
                method = "INSERT"

            log.debug(
                f"Generating UPDATE FK for {table} using fk {key['column']} and parent field {key['parent_table']}.{key['parent_column']}"
            )
            query = f"""
                UPDATE {db_schema}.{table}
                SET {key['column']} = {key['parent_table']}.{key['parent_column']}, method = '{method}'
                FROM {db_schema}.{key['parent_table']}
                WHERE cast({table}.transformation_schema_{key['column']} as int)
                    = cast({key['parent_table']}.transformation_schema_{key['parent_column']} as int);

            """
            update_query += query
    return update_query


@timer
def update_fks(db_config, table_details, match=False):
    query = generate_fk_update_statement(
        db_schema=db_config["target_schema"], table_details=table_details, match=match
    )

    print(f"query: {query}")

    # connection_string = db_config["db_connection_string"]
    # conn = psycopg2.connect(connection_string)
    # cursor = conn.cursor()
    #
    # try:
    #     cursor.execute(query)
    # except Exception as e:
    #     log.debug(e)
    #     os._exit(1)
    # finally:
    #     cursor.close()
    #     conn.commit()
