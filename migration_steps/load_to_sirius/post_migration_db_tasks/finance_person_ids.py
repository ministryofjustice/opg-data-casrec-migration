import logging
import os
import psycopg2
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")
import table_helpers

log = logging.getLogger("root")


def set_invoice_finance_person_ids(cursor):
    if not table_helpers.check_enabled_by_table_name(table_name="finance_invoice"):
        log.info(
            f"Skip setting finance_person_id on invoices. Invoice entity disabled."
        )
        return

    log.info("Setting finance_person_id on invoices...")

    query = f"""
        UPDATE finance_invoice fi
        SET finance_person_id = fp.id
        FROM finance_person fp
        WHERE fi.person_id = fp.person_id
        AND source = 'CASRECMIGRATION'
        AND finance_person_id IS NULL;
    """
    cursor.execute(query)


def set_all_finance_person_ids(db_config):
    connection_string = db_config["target_db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    try:
        set_invoice_finance_person_ids(cursor=cursor)
        conn.commit()
        cursor.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        log.error("There was an error setting Finance Person IDs: %s" % error)
        log.debug(error)
        conn.rollback()
        cursor.close()
        os._exit(1)
