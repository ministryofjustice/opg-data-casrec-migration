from custom_errors import EmptyDataFrame
from utilities.basic_data_table import get_basic_data_table
import logging
import os
import pandas as pd

from helpers import get_mapping_dict, get_table_def
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols

log = logging.getLogger("root")


def insert_annual_report_lodging_details(db_config, target_db, mapping_file):
    chunk_size = db_config["chunk_size"]
    offset = -chunk_size
    chunk_no = 0

    mapping_file_name = f"{mapping_file}_mapping"
    table_definition = get_table_def(mapping_name=mapping_file)

    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    annual_report_logs_query = f'select "id", "c_case", "End Date" from {db_config["target_schema"]}.annual_report_logs;'

    annual_report_logs = pd.read_sql_query(
        annual_report_logs_query, db_config["db_connection_string"]
    )

    while True:
        offset += chunk_size
        chunk_no += 1

        try:
            lodging_details_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            annual_report_lodging_details_joined_df = lodging_details_df.merge(
                annual_report_logs,
                how="inner",
                left_on=["c_case", "c_end_date"],
                right_on=["c_case", "End Date"],
            )

            annual_report_lodging_details_joined_df[
                "annual_report_log_id"
            ] = annual_report_lodging_details_joined_df["id_y"]
            annual_report_lodging_details_joined_df = (
                annual_report_lodging_details_joined_df.drop(columns=["id_y"])
            )
            annual_report_lodging_details_joined_df = (
                annual_report_lodging_details_joined_df.rename(columns={"id_x": "id"})
            )

            annual_report_lodging_details_joined_df = reapply_datatypes_to_fk_cols(
                columns=["annual_report_log_id"],
                df=annual_report_lodging_details_joined_df,
            )

            target_db.insert_data(
                table_name=table_definition["destination_table_name"],
                df=annual_report_lodging_details_joined_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

        except EmptyDataFrame as empty_data_frame:
            if empty_data_frame.empty_data_frame_type == "chunk":
                target_db.create_empty_table(
                    sirius_details=sirius_details, df=empty_data_frame.df
                )
                break
            continue
