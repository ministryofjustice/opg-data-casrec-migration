from typing import List, Dict
import logging

import psycopg2

log = logging.getLogger("root")


def get_table_list():
    return ["persons"]


def get_min_migrated_record(db_config, table, column="id"):
    connection_string = db_config["source_db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    query = f"SELECT min({column}) from {db_config['source_schema']}.{table};"

    try:
        cursor.execute(query)
        min_id = cursor.fetchall()[0][0]
        if min_id:
            log.debug(f"Min staging '{column}' in table '{table}': {min_id}")
            return min_id
        else:
            log.debug(
                f"No data for Sirius '{column}' in table '{table}', setting min_id to 0"
            )
            return 0

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        log.error("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 0


def get_previous_original_record(db_config, table, col_value, column="id"):

    query = f"SELECT max({column}) from {db_config['sirius_schema']}.{table} WHERE {column} < {col_value};"

    connection_string = db_config["sirius_db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        previous_value = cursor.fetchall()[0][0]
        if previous_value:
            log.debug(
                f"Previous Sirius '{column}' in table '{table}': {previous_value}"
            )
            return previous_value
        else:
            log.debug(
                f"No data for previous Sirius '{column}' in table '{table}', setting previous_value to 0"
            )
            return 0

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        log.error("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 0


def check_continuous(table_list, db_config):
    report = {"pass": [], "fail": []}

    for table in table_list:
        first_migrated_record = get_min_migrated_record(
            db_config=db_config, table=table
        )
        last_original_record = get_previous_original_record(
            db_config=db_config, table=table, col_value=first_migrated_record
        )
        if last_original_record + 1 == first_migrated_record:
            report["pass"].append(table)
        else:
            report["fail"].append(table)

    if len(report["fail"]) == 0:
        return (True, report)
    else:
        return (False, report)
