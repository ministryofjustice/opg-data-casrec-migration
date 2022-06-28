from custom_errors import EmptyDataFrame
from utilities.basic_data_table import get_basic_data_table
import json
import logging
import os
import pandas as pd
import re
from datetime import datetime

from helpers import get_mapping_dict, get_table_def
from transform_data.lookup_tables import map_lookup_tables
from utilities.standard_transformations import capitalise_first_letter, first_word

log = logging.getLogger("root")


def _generate_timeline_event_data(
    row: pd.Series,
    current_datetime: datetime = datetime.now(),
    event_sub_type="migration",
) -> str:
    """
    Generate the JSON blob required for timeline_event.event column.
    Uses the Title, Forename, Lastname and Case fields from casrec.pat table.

    Format for the event column is:

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

    See IN-759 for details.

    Title is converted to a salutation via title_codes_lookup
    Forename is transformed with standard_transformations.first_word on pat.Forename
    Surname is transformed with standard_transformations.capitalise_first_letter on pat.Surname
    """
    case = row["c_case"]
    if case is None:
        case = ""

    # current datetime in format 2021-11-23T00:00:00+00:00
    if event_sub_type == "archive":
        event_date = datetime.strptime(
            row["c_away_date"], "%Y-%m-%d %H:%M:%S"
        ).strftime("%Y-%m-%dT00:00:00+00:00")
        subject = "Put Away Notice"
        notes = """
            <p>This case has a put away date and is archived</p>
        """
    else:
        event_date = current_datetime.strftime("%Y-%m-%dT00:00:00+00:00")
        subject = "Migration Notice"
        notes = """
            <p>This case was migrated from casrec, all case notes before this date
            (migrated remarks) are in the case notes tab only</p>
        """
    # name in format "Mr Pete Crawwfford" from Title, Forename, Surname
    name_parts = [row["c_title"], row["c_forename_first"], row["c_surname_caps"]]
    name = " ".join(name_parts).strip()
    name = re.sub(" {2,}", " ", name)

    # personId and personUid will be populated after migration
    return json.dumps(
        {
            "class": "Opg\\Core\\Model\\Event\\Common\\NoteCreated",
            "payload": {
                "isPersonAndCaseEvent": False,
                "isPersonEvent": True,
                "isCaseEvent": False,
                "courtReference": f"{case}",
                "type": "Case note",
                "eventDate": f"{event_date}",
                "subject": f"{subject}",
                "notes": f"{notes}",
                "personType": "Client",
                "personId": "",
                "personUid": "",
                "personName": f"{name}",
                "personCourtRef": f"{case}",
            },
        }
    )


def insert_timeline_events(db_config, target_db, mapping_file, event_sub_type):
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

            # Fix name parts
            timeline_events_df = map_lookup_tables(
                {"c_title": {"lookup_table": "title_codes_lookup"}}, timeline_events_df
            )

            timeline_events_df = capitalise_first_letter(
                "c_surname", "c_surname_caps", timeline_events_df
            )

            timeline_events_df = first_word(
                "c_forename", "c_forename_first", timeline_events_df
            )

            if event_sub_type == "archive":
                timeline_events_df["timestamp"] = timeline_events_df.apply(
                    lambda row: datetime.strptime(
                        row["c_away_date"], "%Y-%m-%d %H:%M:%S"
                    ).strftime("%Y-%m-%dT00:00:00+00:00"),
                    axis=1,
                )

            # Make the JSON in event column
            timeline_events_df["event"] = timeline_events_df.apply(
                lambda row: _generate_timeline_event_data(
                    row=row, event_sub_type=event_sub_type
                ),
                axis=1,
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
