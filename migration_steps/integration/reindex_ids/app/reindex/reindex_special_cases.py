"""
Reindex special cases of columns (or parts of columns)
which act like foreign keys (i.e. refer to columns in
other tables), but where they are not defined as foreign
keys. The main case is properties in JSON columns
which reference IDs in other tables.
"""

import logging
import sys

import psycopg2

from decorators import timer

log = logging.getLogger("root")


@timer
def reindex_special_cases(db_config):
    db_schema = db_config["target_schema"]

    connection_string = db_config["db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    queries = {
        "Updating scheduled_events JSON references to annual_report_logs": f"""
            UPDATE {db_schema}.scheduled_events se
            SET event = jsonb_set(
                jsonb_set(
                    cast(se.event as jsonb),
                    '{{payload, clientId}}',
                    to_jsonb(arl.client_id),
                    false
                ),
                '{{payload, reportingPeriodId}}',
                to_jsonb(arl.id),
                false
            )
            FROM {db_schema}.annual_report_logs arl
            WHERE cast(
                cast(se.event as jsonb)->'payload'->>'reportingPeriodId'
            as int) = cast(arl.transformation_schema_id as int)
            AND se.event->>'class' = 'Opg\\Core\\Model\\Event\\DeputyshipReporting\\ScheduledReportingPeriodEndDate'
            AND se.migration_method = 'INSERT'
        """
    }

    for message, query in queries.items():
        try:
            log.debug(message)
            log.debug(query)
            cursor.execute(query)
        except Exception as e:
            log.debug(e)
            sys.exit(1)
        finally:
            cursor.close()
            conn.commit()
