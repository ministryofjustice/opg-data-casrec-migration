import pandas as pd

from custom_errors import EmptyDataFrame
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table


def do_annual_report_logs_prep(db_config, target_db, mapping_file_name):
    persons_query = (
        f'select "id", "caserecnumber" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_client';"
    )

    return {
        'persons_df': pd.read_sql_query(persons_query, db_config["db_connection_string"])
    }

def get_annual_report_logs_chunk(
    db_config,
    mapping_file_name,
    table_definition,
    sirius_details,
    chunk_size,
    offset,
    prep
):
    try:
        annual_report_log_df = get_basic_data_table(
            db_config=db_config,
            mapping_file_name=mapping_file_name,
            table_definition=table_definition,
            sirius_details=sirius_details,
            chunk_details={"chunk_size": chunk_size, "offset": offset},
        )
    except EmptyDataFrame as e:
        more_records = (e.empty_data_frame_type != 'chunk')
        return (e.df, more_records)

    annual_report_log_joined_df = annual_report_log_df.merge(
        prep["persons_df"],
        how="inner",
        left_on="c_case",
        right_on="caserecnumber",
    )

    annual_report_log_joined_df["client_id"] = annual_report_log_joined_df["id_y"]
    annual_report_log_joined_df = annual_report_log_joined_df.drop(columns=["id_y"])
    annual_report_log_joined_df = annual_report_log_joined_df.rename(columns={"id_x": "id"})

    annual_report_log_joined_df = reapply_datatypes_to_fk_cols(
        columns=["client_id"],
        df=annual_report_log_joined_df
    )

    return (annual_report_log_joined_df, True)
