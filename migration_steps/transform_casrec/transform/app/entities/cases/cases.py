import logging

import pandas as pd
from utilities.basic_data_table import get_basic_data_table

from custom_errors import EmptyDataFrame
from helpers import get_mapping_dict, get_table_def

log = logging.getLogger("root")


CASREC_TO_SIRIUS_DEPUTY_CODES = {
    "1": "SOLE",
    "2": "JOINT",
    "3": "JOINTANDSEVERALLY",
    "4": "JOINTANDSEVERALLY",
}


def _set_sirius_howdeputyappointed_code(row):
    row["howdeputyappointed"] = CASREC_TO_SIRIUS_DEPUTY_CODES.get(
        row["casrec_deputyship_joint"], None
    )
    return row


def insert_cases(db_config, target_db, mapping_file):
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

    # DataFrame for setting howdeputyappointed column.
    # Get a single deputyship record for each case from the casrec deputyship table,
    # where "Joint" != '5'. Where a case has multiple deputies, the "Joint" value
    # for all those deputies should be the same, so just use the first. If it isn't
    # the same, still use the first. If there are no "Joint" values, set it to null.
    deputyships_query = f"""
        SELECT
            "Order No" AS casrec_deputyship_order_no,
            "Joint" AS casrec_deputyship_joint
        FROM (
            SELECT
                "Order No",
                "Joint",
                row_number() OVER (PARTITION BY "Order No" ORDER BY "Create" DESC) AS rownum
            FROM (
                SELECT
                    "Order No",
                    "Joint",
                    "Create"
                FROM {db_config["source_schema"]}.deputyship
                WHERE "Joint" != '5'
            ) AS deputyships
        ) AS numbered_deputyships
        WHERE rownum = 1
    """

    deputyships_df = pd.read_sql_query(
        deputyships_query, db_config["db_connection_string"]
    )

    while True:
        offset += chunk_size
        chunk_no += 1

        try:
            cases_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            # Join to deputyships
            cases_df = cases_df.merge(
                deputyships_df,
                how="left",
                left_on="c_order_no",
                right_on="casrec_deputyship_order_no",
            )

            cases_df = cases_df.apply(_set_sirius_howdeputyappointed_code, axis=1)

            cases_df = cases_df.drop(
                columns=["casrec_deputyship_order_no", "casrec_deputyship_joint"]
            )

            if len(cases_df) > 0:
                target_db.insert_data(
                    table_name=table_definition["destination_table_name"],
                    df=cases_df,
                    sirius_details=sirius_details,
                )

        except EmptyDataFrame as empty_data_frame:
            if empty_data_frame.empty_data_frame_type == "chunk":
                target_db.create_empty_table(
                    sirius_details=sirius_details, df=empty_data_frame.df
                )
                break
            continue
