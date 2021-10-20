import pandas as pd

from custom_errors import EmptyDataFrame
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table

def insert_client_notes(db_config, target_db, mapping_file):
    chunk_size = db_config["chunk_size"]
    offset = -chunk_size
    chunk_no = 0

def do_notes_prep(db_config, target_db, mapping_file_name):
    persons_query = (
        f'select "id", "caserecnumber" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_client';"
    )
    return {
        'persons_df': pd.read_sql_query(persons_query, db_config["db_connection_string"])
    }

def get_notes_chunk(db_config, mapping_file_name, table_definition, sirius_details, chunk_size, offset, prep):
        try:
            notes_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )
        except EmptyDataFrame as e:
            more_records = (e.empty_data_frame_type != 'chunk')
            return (e.df, more_records)

        notes_joined_df = notes_df.merge(
            prep["persons_df"],
            how="left",
            left_on="c_case",
            right_on="caserecnumber"
        )

        notes_joined_df["person_id"] = notes_joined_df["id_y"]
        notes_joined_df = notes_joined_df.drop(columns=["id_y"])
        notes_joined_df = notes_joined_df.rename(columns={"id_x": "id"})

        notes_joined_df = reapply_datatypes_to_fk_cols(
            columns=["person_id"], df=notes_joined_df
        )

        return (notes_joined_df, True)
