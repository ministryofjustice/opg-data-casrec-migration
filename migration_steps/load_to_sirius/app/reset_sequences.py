import sys
from typing import List, Dict
import logging

import psycopg2

log = logging.getLogger("root")


def reset_all_sequences(sequence_list, db_config):
    for seq in sequence_list:
        log.info(f"Resetting sequence {seq['sequence_name']}")
        reset_sequence(sequence_details=seq, db_config=db_config)


def reset_sequence(sequence_details, db_config):

    query = f"""
        SELECT setval('{sequence_details['sequence_name']}', (SELECT MAX ({sequence_details['column']}) FROM {sequence_details['table']}));
    """

    connection_string = db_config["target_db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        log.error("Error: %s" % error)
        conn.rollback()
        cursor.close()
        sys.exit(1)


def reset_all_uid_sequences(uid_sequence_list, db_config):
    for seq in uid_sequence_list:
        log.info(f"Resetting UID sequence {seq['sequence_name']}")
        reset_uid_sequence(sequence_details=seq, db_config=db_config)


def reset_uid_sequence(sequence_details, db_config):
    table_subquery = ""
    for i, table in enumerate(sequence_details["fields"]):
        single_table_subquery = (
            f"SELECT MAX({table['column']}) AS uid FROM {table['table']}"
        )
        if i + 1 < len(sequence_details["fields"]):
            single_table_subquery += " UNION ALL "
        table_subquery += single_table_subquery

    query = f"""
        WITH uids AS (
            {table_subquery}
        )
        SELECT MAX(uid) from uids;
    """

    # log.debug(query)

    connection_string = db_config["target_db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        max_uid = cursor.fetchall()[0][0]

        log.debug(f"max_uid: {max_uid}")

        min_uid = 70000000000
        max_sequence_val = int(str(max_uid)[:-1]) - min_uid

        log.debug(f"max_sequence_val: {max_sequence_val}")

        reset_query = f"""
            SELECT setval('{sequence_details['sequence_name']}', {max_sequence_val});
        """
        # log.debug(reset_query)

        cursor.execute(reset_query)

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        log.error("Error: %s" % error)
        conn.rollback()
        cursor.close()
        sys.exit(1)
