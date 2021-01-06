import pandas as pd

from transform_data import transform
from utilities.generate_source_query import generate_select_string_from_mapping
from helpers import get_mapping_dict


def get_basic_data_table(config, mapping_file_name, table_definition):

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
        source_table_name=table_definition["source_table_name"],
        additional_columns=table_definition["source_table_additional_columns"],
        db_schema=config.etl1_schema,
    )

    source_data_df = pd.read_sql_query(
        sql=source_data_query, con=config.connection_string
    )

    persons_df = transform.perform_transformations(
        mapping_definitions=mapping_dict,
        table_definition=table_definition,
        source_data_df=source_data_df,
        db_conn_string=config.connection_string,
        db_schema=config.etl2_schema,
        sirius_details=sirius_details,
    )

    return sirius_details, persons_df
