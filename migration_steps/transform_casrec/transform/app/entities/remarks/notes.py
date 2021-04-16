from utilities.basic_data_table import get_basic_data_table

definition = {
    "source_table_name": "remarks",
    "source_table_additional_columns": ["Case"],
    "destination_table_name": "notes",
}

mapping_file_name = "notes_mapping"


def insert_notes(db_config, target_db):
    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1

    while True:
        try:
            sirius_details, notes_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=definition,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            if len(notes_df) > 0:
                target_db.insert_data(
                    table_name=definition["destination_table_name"],
                    df=notes_df,
                    sirius_details=sirius_details,
                    chunk_no=chunk_no,
                )

            offset += chunk_size
            chunk_no += 1
        except Exception:
            break
