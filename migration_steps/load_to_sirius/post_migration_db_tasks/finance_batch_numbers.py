import logging
import os
import psycopg2
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")
import table_helpers

log = logging.getLogger("root")


def create_batch_number(cursor):
    log.info("Creating a batch number...")
    query = "UPDATE finance_counter SET counter = counter + 1 WHERE key = 'DatFileBatchNumberReportBatchNumber';"
    cursor.execute(query)

    if cursor.rowcount != 1:
        raise Exception("Error creating a batch number with SQL: %s" % query)

    query = "SELECT counter FROM finance_counter WHERE key = 'DatFileBatchNumberReportBatchNumber'"
    cursor.execute(query)
    result = cursor.fetchone()

    if result is None:
        raise Exception("Unable to fetch batch number with SQL: %s" % query)

    batch_number = result[0]
    log.info("Created batch number: %d" % batch_number)

    return batch_number


def set_batch_number_on_table(cursor, table, batch_number):
    log.info(f"Setting batch number {batch_number} on {table}...")
    query = f"""
        UPDATE {table} SET batchnumber = {batch_number} WHERE batchnumber IS NULL AND source = 'CASRECMIGRATION';
    """
    cursor.execute(query)


def set_all_batch_numbers(db_config):
    connection_string = db_config["target_db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    batch_tables = ["finance_invoice"]

    try:
        for table in batch_tables:
            if not table_helpers.check_enabled_by_table_name(table_name=table):
                log.info(f"Skip setting batch numbers on {table}. Entity disabled.")
                continue
            batch_number = create_batch_number(cursor=cursor)
            set_batch_number_on_table(cursor=cursor, table=table, batch_number=batch_number)
        conn.commit()
        cursor.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        log.error("There was an error setting batch numbers: %s" % error)
        log.debug(error)
        conn.rollback()
        cursor.close()
        os._exit(1)
