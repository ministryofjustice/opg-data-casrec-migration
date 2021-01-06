from utilities.basic_data_table import get_basic_data_table

definition = {
    "sheet_name": "persons (Client)",
    "source_table_name": "pat",
    "source_table_additional_columns": ["Term Type"],
    "destination_table_name": "persons",
}

mapping_file_name = "client_persons_mapping"


def insert_persons_clients(config, etl2_db):

    sirius_details, persons_df = get_basic_data_table(
        config=config, mapping_file_name=mapping_file_name, table_definition=definition
    )

    etl2_db.insert_data(
        table_name=definition["destination_table_name"],
        df=persons_df,
        sirius_details=sirius_details,
    )
