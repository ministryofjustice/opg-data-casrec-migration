import logging

import psycopg2

log = logging.getLogger("root")


def clear_tables(config):
    schema = config.schemas["integration"]
    log.info(f"Clearing tables in schema - {schema}")

    conn = psycopg2.connect(config.get_db_connection_string("migration"))

    cursor = conn.cursor()

    cursor.execute(
        f"""
        SELECT
            table_name
        FROM information_schema.tables
        WHERE table_schema = '{schema}'"""
    )

    tables = [x[0] for x in cursor.fetchall()]

    for t in tables:
        log.log(config.VERBOSE, (f"drop table if exists {schema}.{t};"))
        cursor.execute(f"drop table if exists {schema}.{t};")

    conn.commit()
    cursor.close()
    conn.close()
