from mapping.mapping import Mapping
from transformations import transformations_from_mapping
import pandas as pd


definition = {
    "sheet_name": "persons (Client)",
    "source_table_name": "pat",
    "destination_table_name": "persons",
}


def insert_persons_clients(config, etl2_db):

    mapping_from_excel = Mapping(
        excel_doc=config["mapping_document"]["excel_doc"], table_definitions=definition
    )
    mapping_dict = mapping_from_excel.mapping_definitions()
    source_data_query = mapping_from_excel.generate_select_string_from_mapping()

    source_data_df = pd.read_sql_query(
        sql=source_data_query, con=config["etl2_db"]["connection_string"]
    )

    addresses_df = transformations_from_mapping.perform_transformations(
        mapping_dict, definition, source_data_df, config["etl2_db"]
    )

    etl2_db.insert_data(
        table_name=definition["destination_table_name"], df=addresses_df
    )
