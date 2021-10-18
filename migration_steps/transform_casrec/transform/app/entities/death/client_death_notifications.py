import pandas as pd

from custom_errors import EmptyDataFrame
from helpers import get_mapping_dict, get_table_def
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table


def do_clients_prep(db_config, target_db, mapping_file_name):
    clients_query = (
        f'select "id", "caserecnumber" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_client';"
    )

    return {
        'clients_df': pd.read_sql_query(clients_query, db_config["db_connection_string"])
    }

def get_client_death_notifications_chunk(
        db_config,
        mapping_file_name,
        table_definition,
        sirius_details,
        chunk_size,
        offset,
        prep
):
    try:
        client_death_df = get_basic_data_table(
            db_config=db_config,
            mapping_file_name=mapping_file_name,
            table_definition=table_definition,
            sirius_details=sirius_details,
            chunk_details={"chunk_size": chunk_size, "offset": offset},
        )
    except EmptyDataFrame as e:
        more_records = (e.empty_data_frame_type != 'chunk')
        return (e.df, more_records)

    clients_df = prep['clients_df']

    death_joined_df = client_death_df.merge(
        clients_df, how="left", left_on="c_case", right_on="caserecnumber"
    )

    death_joined_df["person_id"] = death_joined_df["id_y"]
    death_joined_df = death_joined_df.drop(columns=["id_y"])
    death_joined_df = death_joined_df.rename(columns={"id_x": "id"})

    death_joined_df = reapply_datatypes_to_fk_cols(
        columns=["person_id"], df=death_joined_df
    )

    return (death_joined_df, True)
