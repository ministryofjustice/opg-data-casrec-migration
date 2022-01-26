import logging
import pandas as pd

from utilities.basic_data_table import get_basic_data_table

from custom_errors import EmptyDataFrame
from helpers import get_mapping_dict, get_table_def
from transform_data.apply_datatypes import apply_datatypes

log = logging.getLogger("root")


def _set_columns_for_deputy_type(row: pd.Series) -> pd.Series:
    row["organisationname"] = None
    row["deputysubtype"] = None

    if row["deputytype"] == "PUBLICAUTHORITY":
        row["deputysubtype"] = "ORGANISATION"

        # Clear name columns for public authorities

        # Ordering is important for next two lines
        row["organisationname"] = row["surname"]
        row["surname"] = None

        row["salutation"] = None
        row["firstname"] = None
        row["middlenames"] = None

    elif row["deputytype"] == "LAY":
        row["deputysubtype"] = "PERSON"

    return row


def insert_persons_deputies(db_config, target_db, mapping_file):
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
            persons_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            # This has to be done here, as it fails if set
            # in the mapping spreadsheet and automated during get_basic_data_table()
            persons_df["deputycasrecid"] = persons_df["casrec_row_id"]

            # Apply additional transforms manually which depend
            # on whether this is a Lay or PA deputy (see IN-1118)
            persons_df = persons_df.apply(_set_columns_for_deputy_type, axis=1)

            target_db.insert_data(
                table_name=table_definition["destination_table_name"],
                df=persons_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

        except EmptyDataFrame as empty_data_frame:
            if empty_data_frame.empty_data_frame_type == "chunk":
                target_db.create_empty_table(
                    sirius_details=sirius_details, df=empty_data_frame.df
                )
                break
            continue
