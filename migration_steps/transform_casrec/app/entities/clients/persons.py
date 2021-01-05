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

mapping_file_name = "client_persons_mapping"


def insert_persons_clients(config, etl2_db):

    mapping_dict = get_mapping_dict(
        file_name=mapping_file_name, stage_name="transform_casrec"
    )

    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
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

    persons_df = transform.perform_transformations(
        mapping_dict,
        definition,
        source_data_df,
        config.connection_string,
        config.etl2_schema,
        sirius_details,
    )

    etl2_db.insert_data(
        table_name=definition["destination_table_name"],
        df=persons_df,
        sirius_details=sirius_details,
    )
