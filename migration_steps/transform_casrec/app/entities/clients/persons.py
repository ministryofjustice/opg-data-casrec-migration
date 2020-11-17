import json

import pandas as pd

from utilities import transformations_from_mapping
from utilities.generate_source_query import generate_select_string_from_mapping
from utilities.helpers import get_mapping_file, get_mapping_dict

definition = {
    "sheet_name": "persons (Client)",
    "source_table_name": "pat",
    "destination_table_name": "persons",
}


def insert_persons_clients(config, etl2_db):

    mapping_dict = get_mapping_dict(file_name="client_persons_mapping")

    source_data_query = generate_select_string_from_mapping(
        mapping=mapping_dict,
        source_table_name=definition["source_table_name"],
        db_schema=config.etl1_schema,
    )

    source_data_df = pd.read_sql_query(
        sql=source_data_query, con=config.connection_string
    )

    addresses_df = transformations_from_mapping.perform_transformations(
        mapping_dict,
        definition,
        source_data_df,
        config.connection_string,
        config.etl2_schema,
    )

    etl2_db.insert_data(
        table_name=definition["destination_table_name"], df=addresses_df
    )
