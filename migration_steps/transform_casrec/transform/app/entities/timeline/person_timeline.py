from custom_errors import EmptyDataFrame
from utilities.basic_data_table import get_basic_data_table
import json
import logging
import os
import pandas as pd

from helpers import get_mapping_dict, get_table_def

log = logging.getLogger("root")

"""
A case has a single person, and transform.timeline_event has c_case field
with reference to casrec case no. Should then be able to get the Sirius
person ID through persons.caserecnumber.
"""


def insert_person_timeline(db_config, target_db, mapping_file):
    # stub until we get the proper implementation in place
    mapping_file_name = f"{mapping_file}_mapping"
    # table_definition = get_table_def(mapping_name=mapping_file)
    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    df = pd.DataFrame({"id": [], "person_id": [], "timelineevent_id": []})

    target_db.create_empty_table(sirius_details=sirius_details, df=df)
