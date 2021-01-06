import pandas as pd

from utilities.basic_data_table import get_basic_data_table

definition = {
    "source_table_name": "order",
    "source_table_additional_columns": ["Case", "Order No"],
    "destination_table_name": "supervision_level_log",
}

mapping_file_name = "supervision_level_log_mapping"


def insert_supervision_level_log(config, etl2_db):

    sirius_details, supervision_level_df = get_basic_data_table(
        config=config, mapping_file_name=mapping_file_name, table_definition=definition
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
        table_name=definition["destination_table_name"],
        df=supervision_level_joined_df,
        sirius_details=sirius_details,
    )
