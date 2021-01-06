from utilities.basic_data_table import get_basic_data_table

definition = {
    "sheet_name": "cases",
    "source_table_name": "order",
    "source_table_additional_columns": ["Order No"],
    "destination_table_name": "cases",
}
mapping_file_name = "cases_mapping"


def insert_cases(config, etl2_db):

    sirius_details, cases_df = get_basic_data_table(
        config=config, mapping_file_name=mapping_file_name, table_definition=definition
    )

    etl2_db.insert_data(
        table_name=definition["destination_table_name"],
        df=cases_df,
        sirius_details=sirius_details,
    )
