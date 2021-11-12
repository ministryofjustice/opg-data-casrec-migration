from utilities.basic_data_table import get_basic_data_table

import os
import logging

from custom_errors import EmptyDataFrame
from helpers import get_mapping_dict, get_table_def

log = logging.getLogger("root")


def insert_client_nodebtchase_warnings(db_config, target_db, mapping_file):

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
        try:
            offset += chunk_size
            chunk_no += 1

            warnings_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            target_db.insert_data(
                table_name=table_definition["destination_table_name"],
                df=warnings_df,
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

        except Exception as e:
            log.error(f"Unexpected error: {e}")
            os._exit(1)
