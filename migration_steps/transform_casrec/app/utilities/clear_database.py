import logging

import psycopg2

log = logging.getLogger("root")


def clear_tables(config):
    log.info("Clearing tables")

    conn = psycopg2.connect(config.connection_string)

    cursor = conn.cursor()

    cursor.execute(
        f"""
        SELECT
            table_name
        FROM information_schema.tables
        WHERE table_schema = '{config.etl2_schema}'"""
    )

    tables = [x[0] for x in cursor.fetchall()]

    for t in tables:
        log.log(config.VERBOSE, (f"drop table if exists {config.etl2_schema}.{t};"))
        cursor.execute(f"drop table if exists {config.etl2_schema}.{t};")

    conn.commit()
    cursor.close()
    conn.close()
