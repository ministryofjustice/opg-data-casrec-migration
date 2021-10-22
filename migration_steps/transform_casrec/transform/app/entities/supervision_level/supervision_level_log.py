import pandas as pd

from custom_errors import EmptyDataFrame
from utilities.basic_data_table import get_basic_data_table


def do_supervision_level_log_prep(db_config, target_db, mapping_file_name):
    cases_query = f'select "id", "caserecnumber", "c_order_no" from {db_config["target_schema"]}.cases;'

    return {
        'cases_df': pd.read_sql_query(cases_query, db_config["db_connection_string"])
    }

def get_supervision_level_log_chunk(
    db_config,
    mapping_file_name,
    table_definition,
    sirius_details,
    chunk_size,
    offset,
    prep
):
        try:
            supervision_level_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )
        except EmptyDataFrame as e:
            more_records = (e.empty_data_frame_type != 'chunk')
            return (e.df, more_records)

        supervision_level_joined_df = supervision_level_df.merge(
            prep['cases_df'], how="left", left_on="c_order_no", right_on="c_order_no"
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

        return (supervision_level_joined_df, True)
