import pandas as pd
from utilities.basic_data_table import get_basic_data_table

from custom_errors import EmptyDataFrame
from helpers import get_mapping_dict

definition = {
    "source_table_name": "order",
    "source_table_additional_columns": ["Case", "Order No"],
    "destination_table_name": "supervision_level_log",
}

mapping_file_name = "supervision_level_log_mapping"


def insert_supervision_level_log(db_config, target_db):

    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1

    cases_query = f'select "id", "caserecnumber", "c_order_no" from {db_config["target_schema"]}.cases;'
    cases_df = pd.read_sql_query(cases_query, db_config["db_connection_string"])

    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )
    while True:
        try:
            supervision_level_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=definition,
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
                table_name=definition["destination_table_name"],
                df=supervision_level_joined_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )
            offset += chunk_size
            chunk_no += 1
        except EmptyDataFrame:

            target_db.create_empty_table(sirius_details=sirius_details)

            break
        except Exception:
            break
