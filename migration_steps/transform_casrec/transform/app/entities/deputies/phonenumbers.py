import pandas as pd

from custom_errors import EmptyDataFrame
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table


def do_deputies_prep(db_config, target_db, mapping_file_name):
    deputies_query = f"""
        select "id", "c_deputy_no" from {db_config["target_schema"]}.persons
        where "type" = 'actor_deputy';
        """

    return {
        'deputies_df': pd.read_sql_query(deputies_query, db_config["db_connection_string"])
    }

def get_phonenumbers_deputies_chunk(
    db_config,
    mapping_file_name,
    table_definition,
    sirius_details,
    chunk_size,
    offset,
    prep
):
    try:
        phonenos_df = get_basic_data_table(
            db_config=db_config,
            mapping_file_name=mapping_file_name,
            table_definition=table_definition,
            sirius_details=sirius_details,
            chunk_details={"chunk_size": chunk_size, "offset": offset},
        )
    except EmptyDataFrame as e:
        more_records = (e.empty_data_frame_type != 'chunk')
        return (e.df, more_records)

    deputies_df = prep['deputies_df']

    phonenos_joined_df = phonenos_df.merge(
        deputies_df, how="left", left_on="c_deputy_no", right_on="c_deputy_no"
    )

    phonenos_joined_df["person_id"] = phonenos_joined_df["id_y"]
    phonenos_joined_df = phonenos_joined_df.drop(columns=["id_y"])
    phonenos_joined_df = phonenos_joined_df.rename(columns={"id_x": "id"})

    phonenos_joined_df["person_id"] = (
        phonenos_joined_df["person_id"]
        .fillna(0)
        .astype(int)
        .astype(object)
        .where(phonenos_joined_df["person_id"].notnull())
    )

    phonenos_joined_df = reapply_datatypes_to_fk_cols(
        columns=["person_id"], df=phonenos_joined_df
    )

    return (phonenos_joined_df, True)
