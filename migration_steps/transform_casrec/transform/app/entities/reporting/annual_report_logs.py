from custom_errors import EmptyDataFrame
from utilities.basic_data_table import get_basic_data_table
import logging
import os
import pandas as pd

from helpers import get_mapping_dict
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols

log = logging.getLogger("root")

definition = {
    "source_table_name": "account",
    "source_table_additional_columns": ["Case"],
    "destination_table_name": "annual_report_logs",
}

mapping_file_name = "annual_report_logs_mapping"


def insert_annual_report_logs(db_config, target_db):

    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1

    persons_query = (
        f'select "id", "caserecnumber" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_client';"
    )
    persons_df = pd.read_sql_query(persons_query, db_config["db_connection_string"])

    persons_df = persons_df[["id", "caserecnumber"]]

    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )
    while True:
        try:
            annual_report_log_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            annual_report_log_joined_df = annual_report_log_df.merge(
                persons_df,
                how="inner",
                left_on="c_case",
                right_on="caserecnumber",
            )

            annual_report_log_joined_df["client_id"] = annual_report_log_joined_df[
                "id_y"
            ]
            annual_report_log_joined_df = annual_report_log_joined_df.drop(
                columns=["id_y"]
            )
            annual_report_log_joined_df = annual_report_log_joined_df.rename(
                columns={"id_x": "id"}
            )

            annual_report_log_joined_df = reapply_datatypes_to_fk_cols(
                columns=["client_id"], df=annual_report_log_joined_df
            )

            if len(annual_report_log_joined_df) > 0:

                target_db.insert_data(
                    table_name=definition["destination_table_name"],
                    df=annual_report_log_joined_df,
                    sirius_details=sirius_details,
                )

            offset += chunk_size
            chunk_no += 1

        except EmptyDataFrame:

            target_db.create_empty_table(sirius_details=sirius_details)

            break

        except Exception as e:
            log.error(f"Unexpected error: {e}")
            os._exit(1)
