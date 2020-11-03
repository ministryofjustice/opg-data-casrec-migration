import json

import pandas as pd

from utilities import transformations_from_mapping
from utilities.generate_source_query import generate_select_string_from_mapping
from utilities.helpers import get_mapping_file

definition = {
    "sheet_name": "notes",
    "source_table_name": "remarks",
    "source_table_additional_columns": ["Case"],
    "destination_table_name": "notes",
}


def insert_notes(config, etl2_db):

    with open(get_mapping_file(file_name="notes_mapping")) as mapping_json:
        mapping_dict = json.load(mapping_json)

    source_data_query = generate_select_string_from_mapping(
        mapping=mapping_dict,
        source_table_name=definition["source_table_name"],
        additional_columns=definition["source_table_additional_columns"],
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
