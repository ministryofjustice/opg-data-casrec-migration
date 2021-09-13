import logging
import os

import psycopg2

log = logging.getLogger("root")


def get_ids_of_skeleton_persons(db_config):

    connection_string = db_config["sirius_db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    query = f"""
        select id from persons where type in ('actor_client', 'actor_deputy')
        and clientsource='SKELETON' and caseactorgroup != 'CLIENT-PILOT-ONE';
    """

    log.debug(f"Using query: {query}")

    try:
        cursor.execute(query)
        query_result = cursor.fetchall()
        ids = [x[0] for x in query_result]

        return ids

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        log.error(f"error: {error}")
        conn.rollback()
        cursor.close()
        return []


def get_tables_with_fk_links():

    known_tables = [
        {"visits": "client_id"},
        {"supervision_notes": "person_id"},
        {"supervision_notes": "source_clientriskscore_id"},
        {"powerofattorney_person": "person_id"},
        {"phonenumbers": "person_id"},
        {"person_warning": "person_id"},
        {"person_timeline": "person_id"},
        {"person_task": "person_id"},
        {"persons": "parent_id"},
        {"persons": "executor_id"},
        {"persons": "client_id"},
        {"person_research_preferences": "person_id"},
        {"person_personreference": "person_id"},
        {"person_note": "person_id"},
        {"person_document": "person_id"},
        {"person_caseitem": "person_id"},
        {"pa_notified_persons": "notified_person_id"},
        {"pa_certificate_provider": "certificate_provider_id"},
        {"pa_applicants": "person_id"},
        {"order_deputy": "deputy_id"},
        {"investigation": "person_id"},
        {"epa_personnotifydonor": "personnotifydonor_id"},
        {"death_notifications": "person_id"},
        {"cases": "donor_id"},
        {"cases": "feepayer_id"},
        {"cases": "correspondent_id"},
        {"annual_report_logs": "client_id"},
        {"addresses": "person_id"},
        {"bonds": "order_id"},
        {"document_secondaryrecipient": "person_id"},
        {"documents": "correspondent_id"},
        {"cases": "client_id"},
    ]

    return known_tables


def delete_data_with_fk_links(db_config, person_ids):
    tables_with_fks = get_tables_with_fk_links()

    connection_string = db_config["sirius_db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    fk_details = iter(tables_with_fks)
    while True:
        table_details = next(fk_details, "end")
        if table_details == "end":
            break
        ((table, key),) = table_details.items()
        log.debug(f"Generating DELETE for {table} using fk {key}")

        query = f"""delete from {table} where {key} in ({','.join([str(x) for x in person_ids])});"""
        log.debug(f"Delete query: {query}")

        try:
            cursor.execute(query)
            rows_affected = cursor.rowcount

            log.debug(f"Deleted {rows_affected} rows from {table}")

        except (Exception, psycopg2.DatabaseError) as error:
            log.error(f"error: {error}")
            os._exit(1)

    cursor.close()
