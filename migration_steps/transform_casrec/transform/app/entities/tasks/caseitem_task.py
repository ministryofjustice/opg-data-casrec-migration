import pandas as pd

from helpers import get_mapping_dict, get_table_def
from custom_errors import EmptyDataFrame


def insert_caseitem_task(db_config, target_db, mapping_file):
    try:
        sirius_details = get_mapping_dict(
            file_name=f"{mapping_file}_mapping",
            stage_name="sirius_details",
            only_complete_fields=False,
        )

        cases_query = f"SELECT id as caseitem_id, c_order_no FROM {db_config['target_schema']}.cases"
        cases_df = pd.read_sql_query(cases_query, db_config["db_connection_string"])

        tasks_query = (
            f'select id as task_id, c_order_no from {db_config["target_schema"]}.tasks;'
        )
        tasks_df = pd.read_sql_query(tasks_query, db_config["db_connection_string"])

        case_task_df = tasks_df.merge(
            cases_df,
            how="inner",
            left_on="c_order_no",
            right_on="c_order_no",
        )

        case_task_df = case_task_df[["caseitem_id", "task_id"]]
        case_task_df["casrec_details"] = "{}"

        table_definition = get_table_def(mapping_name=mapping_file)
        target_db.insert_data(
            table_name=table_definition["destination_table_name"],
            df=case_task_df,
            sirius_details=sirius_details,
        )
    except EmptyDataFrame as empty_data_frame:
        target_db.create_empty_table(
            sirius_details=sirius_details, df=empty_data_frame.df
        )
