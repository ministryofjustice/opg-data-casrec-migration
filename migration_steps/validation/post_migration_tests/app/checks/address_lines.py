import random
from typing import List, Dict
import logging

import psycopg2

log = logging.getLogger("root")


def get_min_and_max_address_ids(db_config):
    query = f"""
        SELECT min(id), max(id) from {db_config['source_schema']}.addresses
    """

    connection_string = db_config["source_db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    try:
        cursor.execute(query)

        ids = cursor.fetchall()[0]

        if ids:
            log.debug(f"Min & max address ids in staging: {ids[0]}, {ids[1]}")
            return (ids[0], ids[1])
        else:
            log.debug(f"No data for staging min and max address ids, setting both to 0")
            return (0, 0)

        # cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        log.error("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 0


def get_random_address_lines(db_config, min, max, number_of_lines):
    table = "addresses"
    column = "address_lines"

    ids_to_check = random.sample(range(min, max), number_of_lines)
    log.debug(f"Checking ids: {', '.join([str(x) for x in ids_to_check])}")

    query = f"""
        SELECT {column} FROM {table}
        WHERE id in ({', '.join([str(x) for x in ids_to_check])})
    """

    connection_string = db_config["sirius_db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        lines = cursor.fetchall()
        if lines:
            log.debug(f"{number_of_lines} lines retrieved")
            return lines
        else:
            log.debug(
                f"No data for address lines with ids {', '.join([str(x) for x in ids_to_check])}"
            )
            return 0

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        log.error("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 0


def check_address_line_format(db_config, number_of_lines=10):
    min, max = get_min_and_max_address_ids(db_config)

    address_lines = get_random_address_lines(
        db_config=db_config, min=min, max=max, number_of_lines=number_of_lines
    )

    try:
        type_check = [type(x[0]) == list for x in address_lines]
        passes = len([x for x in type_check if x == True])
        fails = len([x for x in type_check if x == False])
        report = {
            "pass": [f"{passes}/{number_of_lines}"],
            "fail": [f"{fails}/{number_of_lines}"],
        }

        if False in type_check:
            return (False, report)
        else:
            return (True, report)
    except Exception:
        report = {"other": "Test failed to run"}
        return (False, report)
