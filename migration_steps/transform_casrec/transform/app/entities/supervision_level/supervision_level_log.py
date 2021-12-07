import pandas as pd
from utilities.basic_data_table import get_basic_data_table

from custom_errors import EmptyDataFrame
from helpers import get_mapping_dict, get_table_def


def insert_supervision_level_log(db_config, target_db, mapping_file):
    chunk_size = db_config["chunk_size"]
    offset = -chunk_size
    chunk_no = 0

    cases_query = f'select "id", "caserecnumber", "c_order_no" from {db_config["target_schema"]}.cases;'
    cases_df = pd.read_sql_query(cases_query, db_config["db_connection_string"])

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
            supervision_level_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            supervision_level_joined_df = supervision_level_df.merge(
                cases_df, how="left", left_on="c_order_no", right_on="c_order_no"
            )

            supervision_level_joined_df["order_id"] = supervision_level_joined_df[
                "id_y"
            ]
            supervision_level_joined_df = supervision_level_joined_df.drop(
                columns=["id_y"]
            )
            supervision_level_joined_df = supervision_level_joined_df.rename(
                columns={"id_x": "id"}
            )

            target_db.insert_data(
                table_name=table_definition["destination_table_name"],
                df=supervision_level_joined_df,
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
