import logging
import os

import psycopg2

log = logging.getLogger("root")


def update_client_id_on_cases(db_config):
    log.info("Updating client_id on cases")

    query = f"""
        with case_client_details as (
            select cases.id as case_id, persons.id as person_id
            from {db_config['target_schema']}.cases
                     left outer join {db_config['target_schema']}.persons
                                     on persons.caserecnumber = cases.caserecnumber and persons.type = 'actor_client'
        )

        update {db_config['target_schema']}.cases
        set client_id = case_client_details.person_id
        from case_client_details
        where cases.id = case_client_details.case_id;
    """

    connection_string = db_config["db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        log.debug(f"Updated {cursor.rowcount} rows")
        conn.commit()

    except (Exception) as error:
        log.error("Error: %s" % error)
        os._exit(1)
    finally:
        cursor.close()
        conn.close()
