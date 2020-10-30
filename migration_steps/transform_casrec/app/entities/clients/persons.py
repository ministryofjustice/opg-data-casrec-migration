import json

import pandas as pd

from utilities import transformations_from_mapping
from utilities.generate_source_query import generate_select_string_from_mapping

definition = {
    "sheet_name": "persons (Client)",
    "source_table_name": "pat",
    "destination_table_name": "persons",
}


def insert_persons_clients(config, etl2_db):

    with open(
        "migration_steps/transform_casrec/app/mapping_definitions"
        "/persons_client_mapping"
        ".json"
    ) as mapping_json:
        mapping_dict = json.load(mapping_json)

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
