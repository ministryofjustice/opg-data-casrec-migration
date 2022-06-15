from custom_errors import EmptyDataFrame
from utilities.basic_data_table import get_basic_data_table
import json
import logging
import os
import pandas as pd

from helpers import get_mapping_dict, get_table_def, get_config
from transform_data.apply_datatypes import apply_datatypes
from transform_data.unique_id import add_unique_id

environment = os.environ.get("ENVIRONMENT")
config = get_config(environment)

log = logging.getLogger("root")

"""
A case has a single person, and transform.timeline_event has c_case field
with reference to casrec case no. We can get the Sirius
person ID through persons.caserecnumber.
"""


def insert_person_timeline(db_config, target_db, mapping_file):
    table_definition = get_table_def(mapping_name=mapping_file)
    sirius_details = get_mapping_dict(
        file_name=f"{mapping_file}_mapping",
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    timeline_event_query = f"""
        SELECT te.id AS timelineevent_id, te.c_case AS timelineevent_case
        FROM {db_config["target_schema"]}.timeline_event te
        WHERE (te.event->'payload'->>'isPersonEvent')::bool IS true AND
        (te.event->'payload'->>'subject') in ('Migration Notice', 'Put Away Notice')
    """

    timeline_event_df = pd.read_sql_query(
        timeline_event_query, db_config["db_connection_string"]
    )

    chunk_size = db_config["chunk_size"]
    offset = -chunk_size
    chunk_no = 0

    table_created = False
    has_more_records = True

    while has_more_records:
        offset += chunk_size
        chunk_no += 1

        try:
            # Get chunk of persons
            persons_query = f"""
                SELECT p.id AS person_id, p.caserecnumber AS person_case,
                p.clientsource AS clientsource
                FROM {db_config["target_schema"]}.persons p
                LIMIT {chunk_size} OFFSET {offset}
            """

            persons_df = pd.read_sql_query(
                persons_query, db_config["db_connection_string"]
            )

            # Dataframe is unfiltered, so if it has no records,
            # we have reached the end of the table
            if len(persons_df) == 0:
                has_more_records = False

                # If we haven't inserted any records yet, table wouldn't have been created,
                # so attempt to create it here. NB we are likely to never reach this code,
                # as we will have at least one record in annual_report_logs which triggers
                # insert_data().
                if not table_created:
                    df = pd.DataFrame(
                        {"id": [], "person_id": [], "timelineevent_id": []}
                    )
                    df = apply_datatypes(mapping_details=sirius_details, df=df)

                    target_db.create_empty_table(sirius_details=sirius_details, df=df)
                    table_created = True
            else:
                # Filter so we only have persons imported during migration
                persons_df = persons_df.loc[
                    persons_df["clientsource"]
                    == str(config.migration_phase["migration_identifier"])
                ]

                # Join to timeline_event on case no.
                persons_df = persons_df.merge(
                    timeline_event_df,
                    how="inner",
                    left_on="person_case",
                    right_on="timelineevent_case",
                )

                # We only need to do additional processing if there are records remaining
                if len(persons_df) > 0:
                    # Drop columns we don't need
                    persons_df.drop(
                        columns=["person_case", "clientsource", "timelineevent_case"]
                    )

                    # Add id column
                    persons_df = add_unique_id(
                        db_conn_string=db_config["db_connection_string"],
                        db_schema=db_config["target_schema"],
                        table_definition=table_definition,
                        source_data_df=persons_df,
                    )

                    persons_df = apply_datatypes(
                        mapping_details=sirius_details, df=persons_df
                    )

                    # Insert into db
                    target_db.insert_data(
                        table_name=table_definition["destination_table_name"],
                        df=persons_df,
                        sirius_details=sirius_details,
                        chunk_no=chunk_no,
                    )

                    table_created = True

        except Exception as e:
            log.error(f"Unexpected error: {e}")
            os._exit(1)
