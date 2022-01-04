import pandas as pd
from custom_errors import EmptyDataFrame

from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table
import logging
import os

from helpers import get_mapping_dict, get_table_def

log = logging.getLogger("root")


def insert_finance_order(target_db, db_config, mapping_file):
    chunk_size = db_config["chunk_size"]
    offset = -chunk_size
    chunk_no = 0

    orders_query = (
        f'SELECT "id" AS order_id, "c_order_no" FROM {db_config["target_schema"]}.cases;'
    )
    orders_df = pd.read_sql_query(orders_query, db_config["db_connection_string"])
    orders_df = orders_df[["order_id", "c_order_no"]]

    risk_assessment_query = (
        f'''
            SET datestyle = "ISO, DMY";
            SELECT MIN("Start Date"::date) AS billing_start_date,
            "Order No" AS c_order_no
            FROM {db_config["source_schema"]}.risk_assessment
            GROUP BY "Order No";
        '''
    )
    risk_assessment_df = pd.read_sql_query(risk_assessment_query, db_config["db_connection_string"])
    risk_assessment_df = risk_assessment_df[["billing_start_date", "c_order_no"]]

    mapping_file_name = f"{mapping_file}_mapping"
    table_definition = get_table_def(mapping_name=mapping_file)
    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )
    while True:
        offset += chunk_size
        chunk_no += 1

        try:
            finance_order_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            finance_order_joined_df = finance_order_df.merge(
                orders_df,
                how="inner",
                left_on="c_order_no",
                right_on="c_order_no",
            )

            finance_order_joined_df = finance_order_joined_df.merge(
                risk_assessment_df,
                how="left",
                left_on="c_order_no",
                right_on="c_order_no",
            )

            finance_order_joined_df = reapply_datatypes_to_fk_cols(
                columns=["order_id"], df=finance_order_joined_df
            )

            target_db.insert_data(
                table_name=table_definition["destination_table_name"],
                df=finance_order_joined_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

        except EmptyDataFrame as empty_data_frame:
            if empty_data_frame.empty_data_frame_type == 'chunk':
                target_db.create_empty_table(sirius_details=sirius_details)
                break
            continue

        except Exception as e:
            log.error(f"Unexpected error: {e}")
            os._exit(1)
