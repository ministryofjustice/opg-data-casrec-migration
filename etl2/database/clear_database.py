import sys
import psycopg2


def clear_tables(config):
    conn = psycopg2.connect(config["etl2_db"]["connection_string"])

    cursor = conn.cursor()

    tables = [
        "persons",
        "addresses",
        "cases",
        "notes",
        "person_caseitem",
        "person_note",
    ]

    for t in tables:
        print(f"drop table if exists {config['etl2_db']['schema_name']}.{t};")
        cursor.execute(f"drop table if exists {config['etl2_db']['schema_name']}.{t};")

    conn.commit()
    cursor.close()
    conn.close()
