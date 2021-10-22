import pandas as pd

from custom_errors import EmptyDataFrame
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table


def do_visits_prep(db_config, target_db, mapping_file_name):
    persons_query = (
        f'select "id", "caserecnumber" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_client';"
    )

    return {
        'persons_df': pd.read_sql_query(persons_query, db_config["db_connection_string"])
    }

def get_visits_chunk(db_config, mapping_file_name, table_definition, sirius_details, chunk_size, offset, prep):
    try:
        visits_df = get_basic_data_table(
            db_config=db_config,
            mapping_file_name=mapping_file_name,
            table_definition=table_definition,
            sirius_details=sirius_details,
            chunk_details={"chunk_size": chunk_size, "offset": offset},
        )
    except EmptyDataFrame as e:
        more_records = (e.empty_data_frame_type != 'chunk')
        return (e.df, more_records)

    visits_joined_df = visits_df.merge(
        prep['persons_df'], how="left", left_on="c_case", right_on="caserecnumber"
    )

    visits_joined_df["client_id"] = visits_joined_df["id_y"]
    visits_joined_df = visits_joined_df.drop(columns=["id_y"])
    visits_joined_df = visits_joined_df.rename(columns={"id_x": "id"})

    visits_joined_df = reapply_datatypes_to_fk_cols(
        columns=["client_id"], df=visits_joined_df
    )

    return (visits_joined_df, True)
