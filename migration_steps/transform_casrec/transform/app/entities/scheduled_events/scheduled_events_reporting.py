import json
import logging
import pandas as pd

from helpers import get_mapping_dict, get_table_def
from transform_data.unique_id import add_unique_id

log = logging.getLogger("root")


def _generate_event_json(row: pd.Series) -> str:
    """
    Generate the JSON blob required for scheduled_events.event column.

    Format for the reporting period end date event is:

    {
        "class":"Opg\\Core\\Model\\Event\\DeputyshipReporting\\ScheduledReportingPeriodEndDate",
        "payload": {
            "clientId": 1,
            "reportingPeriodId": 2,
            "endDate": "2021-11-23T00:00:00+00:00"
        }
    }
    """

    # end date in format 2021-11-23T00:00:00+00:00
    end_date = row["end_date"].strftime("%Y-%m-%dT00:00:00+00:00")

    return json.dumps(
        {
            "class": "Opg\\Core\\Model\\Event\\DeputyshipReporting\\ScheduledReportingPeriodEndDate",
            "payload": {
                "clientId": row['client_id'],
                "reportingPeriodId": row['reporting_period_id'],
                "endDate": f"{end_date}"
            }
        }
    )


def apply_event_column(df: pd.DataFrame) -> pd.DataFrame:
    # create event column
    df['event'] = df.apply(
        _generate_event_json, axis=1
    )

    # drop temp columns used for event json generation
    return df.drop(
        columns=["client_id", "reporting_period_id", "end_date"]
    )


def insert_scheduled_events_reporting(db_config, target_db, mapping_file):
    table_definition = get_table_def(mapping_name=mapping_file)

    sirius_details = get_mapping_dict(
        file_name=f"{mapping_file}_mapping",
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1

    has_more_records = True

    while has_more_records:
        events_query = f"""
            SELECT
                reportingperiodenddate + INTERVAL '1 YEAR - 1 DAY' AS dueby,
                FALSE AS processed,
                1 AS version,
                client_id,
                id AS reporting_period_id,
                reportingperiodenddate + INTERVAL '1 YEAR' AS end_date,
                '{{}}' as event,
                'scheduled_events_reporting_mapping' as casrec_mapping_file_name
            FROM {db_config["target_schema"]}.annual_report_logs
            WHERE status = 'PENDING'
            ORDER BY id
            OFFSET {offset} LIMIT {chunk_size}
        """

        events_df = pd.read_sql_query(
            events_query, db_config["db_connection_string"]
        )

        # Dataframe is unfiltered, so if it has no records,
        # we have reached the end of the annual_report_logs table
        if len(events_df) == 0:
            has_more_records = False

            # If we haven't inserted any records yet, table wouldn't have been created,
            # so attempt to create it here. NB we are likely to never reach this code,
            # as we will have at least one record in annual_report_logs which triggers
            # insert_data().
            if chunk_no == 1:
                target_db.create_empty_table(
                    sirius_details=sirius_details, df=events_df
                )
        else:
            # Add an id column (because we haven't used the get_basic_data_table() function,
            # we have to do it manually)
            events_df = add_unique_id(
                db_conn_string=db_config["db_connection_string"],
                db_schema=db_config["target_schema"],
                table_definition=table_definition,
                source_data_df=events_df,
            )

            events_df = apply_event_column(events_df)

            target_db.insert_data(
                table_name=table_definition["destination_table_name"],
                df=events_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

        offset += chunk_size
        chunk_no += 1
