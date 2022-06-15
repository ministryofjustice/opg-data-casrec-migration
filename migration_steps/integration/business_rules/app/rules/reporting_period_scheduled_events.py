import logging
import os

import psycopg2

log = logging.getLogger("root")


def update_report_log_scheduled_events_foreign_keys(db_config):
    log.info(
        "Updating foreign keys in JSON col scheduled_events.event for annual report log events"
    )

    query = f"""
        WITH report_logs AS (
                SELECT id AS report_log_id,
                    transformation_schema_id AS old_report_log_id,
                    client_id,
                    transformation_schema_client_id AS old_client_id
                FROM integration.annual_report_logs
            )

        UPDATE integration.scheduled_events
        SET event = jsonb_set(
            event::jsonb,
            '{{payload}}',
            (event->'payload')::jsonb
                || CONCAT(
                    '{{"clientId":', client_id, ', "reportingPeriodId":', report_log_id, '}}'
                )::jsonb
        )
        FROM report_logs
        WHERE report_logs.old_report_log_id = (scheduled_events.event->'payload'->>'reportingPeriodId')::int
          AND report_logs.old_client_id = (scheduled_events.event->'payload'->>'clientId')::int
          AND scheduled_events.casrec_mapping_file_name = 'scheduled_events_reporting_mapping';
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
