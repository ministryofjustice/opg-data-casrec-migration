import logging

import psycopg2

log = logging.getLogger("root")


def update_deputy_feepayer_id(db_config):
    log.info("Updating feepayer id on clients")

    query = f"""

        alter table {db_config['target_schema']}.persons add column feepayer_id int;

        with feepayer_details as (
                select persons.id as person_id,  order_deputy.deputy_id
                from {db_config['target_schema']}.persons
                left outer join {db_config['target_schema']}.person_caseitem on persons.id = person_caseitem.person_id
                left outer join {db_config['target_schema']}.order_deputy
                    on person_caseitem.caseitem_id = order_deputy.order_id and order_deputy.c_fee_payer = 'Y'
                where persons.type='actor_client'
                and order_deputy.deputy_id is not null
            )

        update {db_config['target_schema']}.persons
        set feepayer_id = cast(deputy_id as int)
        from feepayer_details
        where feepayer_details.person_id = persons.id;
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
    finally:
        cursor.close()
        conn.close()
