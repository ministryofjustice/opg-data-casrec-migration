from custom_errors import EmptyDataFrame
from utilities.basic_data_table import get_basic_data_table
import json
import logging
import os

from helpers import get_mapping_dict, get_table_def

log = logging.getLogger("root")


def _generate_timeline_event_data(row):
    """
    Generate the JSON blob required for timeline_event entries.
    Uses the Title, Forename, Lastname and Case fields from casrec.pat table.

    {
        "class":"Opg\\Core\\Model\\Event\\Common\\NoteCreated",
        "payload": {
            "isPersonAndCaseEvent": false,
            "isPersonEvent": true,
            "isCaseEvent": false,
            "courtReference": "{PAT.Case}",
            "type": "Case note",
            "eventDate": "{current datetime in format 2021-11-23T00:00:00+00:00}",
            "subject": "Migration Notice",
            "notes": "<p>This case was migrated from casrec, all case notes before this date (migrated remarks) are in the case notes tab only</p>",
            "personType": "Client",
            "personId": "{empty string, to be populated after migration}",
            "personUid": "{empty string, to be populated after migration}",
            "personName": "{name in format "Mr Andrew Crawford" from Title, Forename, Surname}" ,
            "personCourtRef": "{PAT.Case}"
        }
    }

    Title comes from title_codes_lookup
    Forename will need transform first_word on pat.Forename
    Surname will need transform capitalise_first_letter on pat.Surname
    """
    return json.dumps({"set_by_fn": True})


def insert_timeline_events(db_config, target_db, mapping_file):
    chunk_size = db_config["chunk_size"]
    offset = -chunk_size
    chunk_no = 0

    mapping_file_name = f"{mapping_file}_mapping"
    table_definition = get_table_def(mapping_name=mapping_file)
    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    while True:
        offset += chunk_size
        chunk_no += 1

        try:
            timeline_events_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            timeline_events_df["event"] = timeline_events_df.apply(
                _generate_timeline_event_data, axis=1
            )

            if len(timeline_events_df) > 0:
                target_db.insert_data(
                    table_name=table_definition["destination_table_name"],
                    df=timeline_events_df,
                    sirius_details=sirius_details,
                )

        except EmptyDataFrame as empty_data_frame:
            if empty_data_frame.empty_data_frame_type == "chunk":
                target_db.create_empty_table(
                    sirius_details=sirius_details, df=empty_data_frame.df
                )
                break
            continue

        except Exception as e:
            log.error(f"Unexpected error: {e}")
            log.exception(e)
            os._exit(1)
