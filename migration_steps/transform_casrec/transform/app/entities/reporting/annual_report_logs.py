from custom_errors import EmptyDataFrame
from utilities.basic_data_table import get_basic_data_table
import logging
import os

from helpers import get_mapping_dict

log = logging.getLogger("root")

definition = {
    "source_table_name": "account",
    "source_table_additional_columns": [],
    "destination_table_name": "annual_report_log",
}

mapping_file_name = "annual_report_logs_mapping"


def insert_annual_report_logs(db_config, target_db):

    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1

    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )
    while True:
        try:
            annual_report_log_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            target_db.insert_data(
                table_name=definition["destination_table_name"],
                df=annual_report_log_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

            offset += chunk_size
            chunk_no += 1

        except EmptyDataFrame:

            target_db.create_empty_table(sirius_details=sirius_details)

            break

        except Exception as e:
            log.error(f"Unexpected error: {e}")
            os._exit(1)
