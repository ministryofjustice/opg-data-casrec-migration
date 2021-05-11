from utilities.basic_data_table import get_basic_data_table
import numpy as np

definition = {
    "source_table_name": "deputy",
    "source_table_additional_columns": [],
    "destination_table_name": "deputy_violent_warnings",
}

mapping_file_name = "deputy_violent_warnings_mapping"


def insert_deputy_violent_warnings(db_config, target_db):

    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1

    while True:
        try:
            sirius_details, warnings_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=definition,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            warnings_df = warnings_df.replace("", np.nan)
            remove_null_cols = ["warningtype", "warningtext"]
            warnings_df = warnings_df.dropna(
                subset=remove_null_cols, thresh=len(remove_null_cols)
            )

            target_db.insert_data(
                table_name=definition["destination_table_name"],
                df=warnings_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

            offset += chunk_size
            chunk_no += 1

        except Exception:
            break
