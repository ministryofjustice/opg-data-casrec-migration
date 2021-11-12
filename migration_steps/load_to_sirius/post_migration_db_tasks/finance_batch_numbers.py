import logging
import os
import psycopg2
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")
import table_helpers
import helpers

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


def set_batch_numbers_in_migrated_tables(cursor):
    batch_tables = [["finance_invoice"], ["finance_ledger", "finance_ledger_allocation"]]

    for tables in batch_tables:
        batch_number = None
        for table in tables:
            if not table_helpers.check_enabled_by_table_name(table_name=table):
                log.info(f"Skip setting batch numbers in {table}. Entity disabled.")
                continue
            if batch_number is None:
                batch_number = create_batch_number(cursor=cursor)

            log.info(f"Setting batch number {batch_number} in {table}...")
            query = f"""
                    UPDATE {table} SET batchnumber = {batch_number} WHERE batchnumber IS NULL AND source = 'CASRECMIGRATION';
                """
            cursor.execute(query)


def set_batch_numbers_in_finance_person(cursor):
    if not helpers.check_entity_enabled(entity_name="clients"):
        log.info(f"Skip setting batch numbers in finance_person. Clients entity disabled.")
        return

    batch_number = create_batch_number(cursor=cursor)

    log.info(f"Setting batch number {batch_number} in finance_person...")
    query = f"""
        UPDATE finance_person
        SET batchnumber = {batch_number}
        FROM persons
        WHERE finance_person.person_id = persons.id
        AND persons.type = 'actor_client'
        AND persons.clientsource = 'CASRECMIGRATION'
        AND finance_person.batchnumber IS NULL;
    """
    cursor.execute(query)


def set_all_batch_numbers(db_config):
    connection_string = db_config["target_db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    try:
        set_batch_numbers_in_migrated_tables(cursor=cursor)
        set_batch_numbers_in_finance_person(cursor=cursor)

        conn.commit()
        cursor.close()
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        log.error("There was an error setting batch numbers: %s" % error)
        log.debug(error)
        conn.rollback()
        cursor.close()
        os._exit(1)
