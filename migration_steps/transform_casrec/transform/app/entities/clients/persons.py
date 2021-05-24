from custom_errors import EmptyDataFrame
from utilities.basic_data_table import get_basic_data_table
import logging
import os


log = logging.getLogger("root")

definition = {
    "source_table_name": "pat",
    "source_table_additional_columns": ["Term Type"],
    "destination_table_name": "persons",
}

mapping_file_name = "client_persons_mapping"


def insert_persons_clients(db_config, target_db):

    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1

    while True:
        try:
            sirius_details, persons_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=definition,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            target_db.insert_data(
                table_name=definition["destination_table_name"],
                df=persons_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

            offset += chunk_size
            chunk_no += 1

        except EmptyDataFrame as e:
            log.debug(e)
            break
        except Exception as e:
            log.error(f"Unexpected error: {e}")
            os._exit(1)
