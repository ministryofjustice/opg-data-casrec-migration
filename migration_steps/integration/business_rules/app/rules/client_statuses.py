import logging
import psycopg2
import os

log = logging.getLogger("root")
client_status_lkp_table = "client_status_lookup"

environment = os.environ.get("ENVIRONMENT")
import helpers

config = helpers.get_config(env=environment)


def get_select_statuses_query(db_config):

    death_status_query = f"""
        SELECT
        person_id,
        CASE WHEN datenotified is not null THEN 'DEATH_NOTIFIED' end AS death_notified_status,
        CASE WHEN proofofdeathreceived THEN 'DEATH_CONFIRMED' end AS death_proof_status
        FROM {db_config['target_schema']}.death_notifications"""

    active_exists_status_query = f"""
        SELECT distinct
        orderstatus AS has_active_status,
        client_id
        FROM {db_config["target_schema"]}.cases
        WHERE orderstatus = 'ACTIVE'"""

    latest_order_status_query = f"""
        SELECT client_id, orderstatus AS status_latest,
        orderclosurereason AS closure_reason, ordersubtype AS order_sub_type
        FROM (
            SELECT row_number() over (partition by client_id ORDER BY orderdate DESC) AS rown,
            orderstatus,
            orderclosurereason,
            client_id,
            ordersubtype
            FROM {db_config["target_schema"]}.cases
        ) AS a
        WHERE rown = 1"""

    identical_order_status_query = f"""
        SELECT DISTINCT c.client_id, c.orderstatus AS identical_status
        FROM {db_config["target_schema"]}.cases c inner join
        (
            SELECT client_id
            FROM {db_config["target_schema"]}.cases
            group by client_id
            having max(orderstatus) = min(orderstatus)
        ) AS co on c.client_id = co.client_id"""

    all_closed_or_dup_status_query = f"""
        SELECT client_id, \'CLOSED\' AS closed_dup_status
        FROM {db_config["target_schema"]}.cases
        group by client_id
        having count(*) = count(
            CASE
            WHEN orderstatus = 'CLOSED' THEN 'X'
            WHEN orderstatus = 'DUPLICATE' THEN 'X'
            end
        )"""

    full_sql = f"""SELECT
    client.id AS id,
    has_active_status.has_active_status AS has_active_status,
    latest_status.status_latest AS latest_status,
    identical_status.identical_status AS identical_status,
    closed_dup_status.closed_dup_status AS closed_dup_status,
    death_status.death_notified_status AS death_notified_status,
    death_status.death_proof_status AS death_proof_status,
    latest_status.closure_reason AS closure_reason,
    latest_status.order_sub_type AS order_sub_type
    FROM
    {db_config["target_schema"]}.persons AS client
    left join ({death_status_query}
    ) AS death_status on death_status.person_id = client.id
    left join ({latest_order_status_query}
    ) AS latest_status on latest_status.client_id = client.id
    left join ({identical_order_status_query}
    ) AS identical_status on identical_status.client_id = client.id
    left join ({all_closed_or_dup_status_query}
    ) AS closed_dup_status on closed_dup_status.client_id = client.id
    left join ({active_exists_status_query}
    ) AS has_active_status on has_active_status.client_id = client.id
    WHERE
    client.type = 'actor_client'
    AND client.clientsource = '{config.migration_phase["migration_identifier"]}'
    ORDER BY client.id"""

    log.info(full_sql)

    return full_sql


def create_client_status_table(db_config, cursor, conn):
    create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {db_config["target_schema"]}.{client_status_lkp_table} (
        id int,
        has_active_status text default NULL,
        latest_status text default NULL,
        identical_status text default NULL,
        closed_dup_status text default NULL,
        death_notified_status text default NULL,
        death_proof_status text default NULL,
        closure_reason text default NULL,
        order_sub_type text default NULL,
        final_client_status text default NULL
    );"""

    cursor.execute(create_table_sql)

    insert_sql = f"""
        insert into {db_config["target_schema"]}.{client_status_lkp_table}
        (id, has_active_status, latest_status, identical_status, closed_dup_status,
        death_notified_status, death_proof_status, closure_reason, order_sub_type)
        {get_select_statuses_query(db_config)}
    """

    cursor.execute(insert_sql)
    conn.commit()


def update_client_statuses_table(db_config, cursor, conn):
    update_sql = f"""
        UPDATE {db_config["target_schema"]}.{client_status_lkp_table}
        SET final_client_status =
        CASE
            WHEN death_notified_status = 'DEATH_NOTIFIED' THEN 'DEATH_NOTIFIED'
            WHEN death_proof_status = 'DEATH_CONFIRMED' THEN 'DEATH_CONFIRMED'
            WHEN has_active_status = 'ACTIVE' THEN 'ACTIVE'
            WHEN latest_status = 'OPEN' THEN 'OPEN'
            WHEN closed_dup_status = 'CLOSED'
                AND order_sub_type in ('NEW DEPUTY', 'INTERIM ORDER', 'REPLACEMENT', 'SUPPLEMENTARY') THEN 'CLOSED'
            WHEN latest_status = 'CLOSED'
                AND closure_reason = 'REGAINED_CAPACITY'
                THEN 'REGAINED_CAPACITY'
            WHEN latest_status = 'CLOSED'
                AND COALESCE(closure_reason, '') != 'REGAINED_CAPACITY'
                THEN 'INACTIVE'
            WHEN identical_status = 'DUPLICATE' THEN 'DUPLICATE'
            ELSE NULL
        END"""

    cursor.execute(update_sql)
    conn.commit()


def update_persons_client_status(db_config, cursor, conn):
    update_sql = f"""
        UPDATE {db_config["target_schema"]}.persons p
        SET clientstatus = final_client_status
        FROM {db_config["target_schema"]}.{client_status_lkp_table} AS lkp
        WHERE lkp.id = p.id"""

    cursor.execute(update_sql)
    conn.commit()


def update_client_status(db_config):
    connection_string = db_config["db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    log.info(
        f'Creating client status lookup table named: {db_config["target_schema"]}.{client_status_lkp_table}'
    )
    create_client_status_table(db_config, cursor, conn)
    log.info(
        f'Update {db_config["target_schema"]}.{client_status_lkp_table} with final status to use'
    )
    update_client_statuses_table(db_config, cursor, conn)
    log.info(f'Update {db_config["target_schema"]}.persons table with clientstatus')
    update_persons_client_status(db_config, cursor, conn)
    log.info(f'Finished updating {db_config["target_schema"]}.persons table')

    cursor.close()
    conn.close()
