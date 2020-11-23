import pandas as pd

from utilities import transformations_from_mapping
from utilities.generate_source_query import generate_select_string_from_mapping
from utilities.helpers import get_mapping_dict

definition = {
    "source_table_name": "order",
    "source_table_additional_columns": ["Case", "Order No"],
    "destination_table_name": "supervision_level_log",
}


def insert_supervision_level_log(config, etl2_db):

    mapping_dict = get_mapping_dict(file_name="supervision_level_log_mapping")

    source_data_query = generate_select_string_from_mapping(
        mapping=mapping_dict,
        source_table_name=definition["source_table_name"],
        additional_columns=definition["source_table_additional_columns"],
        db_schema=config.etl1_schema,
    )

    source_data_df = pd.read_sql_query(
        sql=source_data_query, con=config.connection_string
    )

    supervision_level_df = transformations_from_mapping.perform_transformations(
        mapping_dict,
        definition,
        source_data_df,
        config.connection_string,
        config.etl2_schema,
    )

    supervision_level_df["order_id"] = supervision_level_df["id"]

    etl2_db.insert_data(
        table_name=definition["destination_table_name"], df=supervision_level_df
    )
