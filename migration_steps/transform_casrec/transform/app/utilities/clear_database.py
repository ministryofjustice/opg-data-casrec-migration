import logging

import psycopg2

log = logging.getLogger("root")


def clear_tables(db_config):
    log.info(f"Clearing tables in '{db_config['target_schema']}' schema")

    conn = psycopg2.connect(db_config["db_connection_string"])

    cursor = conn.cursor()

    cursor.execute(
        f"""
        SELECT
            table_name
        FROM information_schema.tables
        WHERE table_schema = '{db_config['target_schema']}'"""
    )

    tables = [x[0] for x in cursor.fetchall()]

    for t in tables:
        log.log(5, (f"drop table if exists {db_config['target_schema']}.{t};"))
        cursor.execute(f"drop table if exists {db_config['target_schema']}.{t};")

    conn.commit()
    cursor.close()
    conn.close()
