import sys
import psycopg2


def clear_tables(config):
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
    ]

    for t in tables:
        print(f"drop table if exists {config.etl2_schema}.{t};")
        cursor.execute(f"drop table if exists {config.etl2_schema}.{t};")

    conn.commit()
    cursor.close()
    conn.close()
