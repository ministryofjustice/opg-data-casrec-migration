import logging
import os
import psycopg2

from table_helpers import check_enabled_by_table_name

environment = os.environ.get("ENVIRONMENT")
import helpers

config = helpers.get_config(env=environment)

log = logging.getLogger("root")


def set_invoice_finance_person_ids(db_config, cursor):
    if not check_enabled_by_table_name(table_name="finance_invoice"):
        log.info(
            f"Skip setting finance_person_id on invoices. Invoice entity disabled."
        )
        return

    log.info("Setting finance_person_id on invoices...")

    query = f"""
        UPDATE {db_config['target_schema']}.finance_invoice fi
        SET finance_person_id = fp.id
        FROM {db_config['target_schema']}.finance_person fp
        WHERE fi.person_id = fp.person_id;
    """
    cursor.execute(query)


def set_ledger_finance_person_ids(db_config, cursor):
    if not check_enabled_by_table_name(table_name="finance_ledger"):
        log.info(f"Skip setting finance_person_id on ledger. Ledger entity disabled.")
        return

    log.info("Setting finance_person_id on ledger...")

    query = f"""
        WITH ledger_person AS (
            SELECT finance_person_id, ledger_entry_id
            FROM {db_config['target_schema']}.finance_invoice fi
            INNER JOIN {db_config['target_schema']}.finance_ledger_allocation fla ON fi.id = fla.invoice_id
        )

        UPDATE {db_config['target_schema']}.finance_ledger fl
        SET finance_person_id = lp.finance_person_id
        FROM ledger_person AS lp
        WHERE lp.ledger_entry_id = id;
    """
    cursor.execute(query)


def set_fee_reduction_finance_person_ids(db_config, cursor):
    if not check_enabled_by_table_name(table_name="finance_remission_exemption"):
        log.info(
            f"Skip setting finance_person_id on fee reductions. Fee reductions entity disabled."
        )
        return

    log.info("Setting finance_person_id on fee reductions...")

    query = f"""
        SELECT COUNT(*) FROM {db_config['target_schema']}.finance_remission_exemption;
    """
    cursor.execute(query)
    result = cursor.fetchone()

    if result[0] > 0:
        query = f"""
            WITH fee_reduction_person AS (
                SELECT fp.id, p.caserecnumber
                FROM {db_config['target_schema']}.finance_person fp
                INNER JOIN {db_config['target_schema']}.persons p ON p.id = fp.person_id
            )

            UPDATE {db_config['target_schema']}.finance_remission_exemption fre
            SET finance_person_id = frp.id
            FROM fee_reduction_person frp
            WHERE fre.c_case = frp.caserecnumber;
        """
        cursor.execute(query)


def set_finance_order_finance_person_ids(db_config, cursor):
    if not check_enabled_by_table_name(table_name="finance_order"):
        log.info(
            f"Skip setting finance_person_id on finance_order. Finance Order entity disabled."
        )
        return

    log.info("Setting finance_person_id on finance_order...")

    query = f"""
        WITH order_person AS (
            SELECT cases.id, finance_person.id AS finance_person_id
            FROM {db_config['target_schema']}.cases
            INNER JOIN {db_config['target_schema']}.finance_person ON cases.client_id = finance_person.person_id
            INNER JOIN {db_config['target_schema']}.persons ON cases.client_id = persons.id
            WHERE persons.type = 'actor_client'
            AND persons.clientsource = '{config.migration_phase["migration_identifier"]}'
            AND cases.casetype = 'ORDER'
        )

        UPDATE {db_config['target_schema']}.finance_order fo
        SET finance_person_id = op.finance_person_id
        FROM order_person AS op
        WHERE op.id = order_id
        AND fo.finance_person_id IS NULL;
    """
    cursor.execute(query)


def set_finance_person_ids(db_config):
    connection_string = db_config["db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    try:
        set_invoice_finance_person_ids(db_config=db_config, cursor=cursor)
        set_ledger_finance_person_ids(db_config=db_config, cursor=cursor)
        set_fee_reduction_finance_person_ids(db_config=db_config, cursor=cursor)
        set_finance_order_finance_person_ids(db_config=db_config, cursor=cursor)
        conn.commit()
        cursor.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        log.error("There was an error setting Finance Person IDs: %s" % error)
        log.debug(error)
        conn.rollback()
        cursor.close()
        os._exit(1)
