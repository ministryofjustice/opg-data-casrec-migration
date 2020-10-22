import json

from mapping.mapping import Mapping
from transformations import transformations_from_mapping
import pandas as pd

from transformations.generate_source_query import generate_select_string_from_mapping

definition = {
    "sheet_name": "cases",
    "source_table_name": "order",
    "source_table_additional_columns": ["Order No"],
    "destination_table_name": "cases",
}


def insert_cases(config, etl2_db):

    with open("tables/cases/mapping.json") as mapping:
        mapping_dict = json.load(mapping)

    source_data_query = generate_select_string_from_mapping(
        mapping=mapping_dict,
        source_table_name=definition["source_table_name"],
        db_schema=config.etl1_schema,
    )

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
