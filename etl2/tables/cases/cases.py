from mapping.mapping import Mapping
from transformations import transformations_from_mapping
import pandas as pd


definition = {
    "sheet_name": "cases",
    "source_table_name": "order",
    "source_table_additional_columns": ["Order No"],
    "destination_table_name": "cases",
}


def insert_cases(config, etl2_db):

    mapping_from_excel = Mapping(
        excel_doc=config.mapping_document, table_definitions=definition
    )
    mapping_dict = mapping_from_excel.mapping_definitions()
    source_data_query = mapping_from_excel.generate_select_string_from_mapping()

    source_data_df = pd.read_sql_query(
        sql=source_data_query, con=config.connection_string
    )

    final_df = transformations_from_mapping.perform_transformations(
        mapping_dict,
        definition,
        source_data_df,
        config.connection_string,
        config.etl2_schema,
    )

    etl2_db.insert_data(table_name=definition["destination_table_name"], df=final_df)
