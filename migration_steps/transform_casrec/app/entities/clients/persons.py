import pandas as pd

from transform_data import transform
from utilities.generate_source_query import generate_select_string_from_mapping
from helpers import get_mapping_dict

definition = {
    "sheet_name": "persons (Client)",
    "source_table_name": "pat",
    "source_table_additional_columns": ["Term Type"],
    "destination_table_name": "persons",
}


def insert_persons_clients(config, etl2_db):

    mapping_dict = get_mapping_dict(
        file_name="client_persons_mapping", stage_name="transform_casrec"
    )

    source_data_query = generate_select_string_from_mapping(
        mapping=mapping_dict,
        source_table_name=definition["source_table_name"],
        additional_columns=definition["source_table_additional_columns"],
        db_schema=config.etl1_schema,
    )

    source_data_df = pd.read_sql_query(
        sql=source_data_query, con=config.connection_string
    )

    addresses_df = transform.perform_transformations(
        mapping_dict,
        definition,
        source_data_df,
        config.connection_string,
        config.etl2_schema,
    )

    etl2_db.insert_data(
        table_name=definition["destination_table_name"], df=addresses_df
    )
