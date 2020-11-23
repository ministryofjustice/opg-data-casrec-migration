import logging

import psycopg2

log = logging.getLogger("root")


def clear_tables(config):
    log.info("Clearing tables")

    conn = psycopg2.connect(config.connection_string)

    cursor = conn.cursor()

    tables = [
        "persons",
        "addresses",
        "cases",
        "notes",
        "person_caseitem",
        "person_note",
        "order_deputy",
        "phonenumbers",
        "supervision_level_log",
    ]

    for t in tables:
        log.log(config.VERBOSE, (f"drop table if exists {config.etl2_schema}.{t};"))
        cursor.execute(f"drop table if exists {config.etl2_schema}.{t};")

    conn.commit()
    cursor.close()
    conn.close()
