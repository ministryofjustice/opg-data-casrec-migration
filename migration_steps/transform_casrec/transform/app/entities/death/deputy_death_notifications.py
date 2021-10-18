import pandas as pd

from custom_errors import EmptyDataFrame
from helpers import get_mapping_dict, get_table_def
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table


def do_deputies_prep(db_config, target_db, mapping_file_name):
    deputies_query = (
        f'select "id", "c_deputy_no" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_deputy';"
    )

    return {
        'deputies_df': pd.read_sql_query(deputies_query, db_config["db_connection_string"])
    }

def get_deputy_death_notifications_chunk(
        db_config,
        mapping_file_name,
        table_definition,
        sirius_details,
        chunk_size,
        offset,
        prep
):
    try:
        deputy_death_df = get_basic_data_table(
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

    death_joined_df = deputy_death_df.merge(
        deputies_df, how="left", left_on="c_deputy_no", right_on="c_deputy_no"
    )

    death_joined_df["person_id"] = death_joined_df["id_y"]
    death_joined_df = death_joined_df.drop(columns=["id_y"])
    death_joined_df = death_joined_df.rename(columns={"id_x": "id"})

    death_joined_df = reapply_datatypes_to_fk_cols(
        columns=["person_id"], df=death_joined_df
    )

    return (death_joined_df, True)
