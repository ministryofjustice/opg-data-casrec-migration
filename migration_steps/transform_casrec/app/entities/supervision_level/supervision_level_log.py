import pandas as pd

from utilities import transformations_from_mapping
from utilities.generate_source_query import generate_select_string_from_mapping
from helpers import get_mapping_dict

definition = {
    "source_table_name": "order",
    "source_table_additional_columns": ["Case", "Order No"],
    "destination_table_name": "supervision_level_log",
}


def insert_supervision_level_log(config, etl2_db):

    mapping_dict = get_mapping_dict(
        file_name="supervision_level_log_mapping", stage_name="transform_casrec"
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

    supervision_level_df = transformations_from_mapping.perform_transformations(
        mapping_dict,
        definition,
        source_data_df,
        config.connection_string,
        config.etl2_schema,
    )

    cases_query = f'select "id", "caserecnumber", "c_order_no" from etl2.cases;'
    cases_df = pd.read_sql_query(cases_query, config.connection_string)

    supervision_level_joined_df = supervision_level_df.merge(
        cases_df, how="left", left_on="c_order_no", right_on="c_order_no"
    )

    supervision_level_joined_df["order_id"] = supervision_level_joined_df["id_y"]
    supervision_level_joined_df = supervision_level_joined_df.drop(columns=["id_y"])
    supervision_level_joined_df = supervision_level_joined_df.rename(
        columns={"id_x": "id"}
    )

    etl2_db.insert_data(
        table_name=definition["destination_table_name"], df=supervision_level_joined_df
    )
