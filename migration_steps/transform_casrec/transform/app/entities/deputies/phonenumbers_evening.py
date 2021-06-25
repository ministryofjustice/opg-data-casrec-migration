import pandas as pd

from custom_errors import EmptyDataFrame
from helpers import get_mapping_dict
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table

definition = {
    "source_table_name": "deputy",
    "source_table_additional_columns": ["Deputy No"],
    "destination_table_name": "phonenumbers",
}

mapping_file_name = "deputy_evening_phonenumbers_mapping"


def insert_phonenumbers_deputies_evening(db_config, target_db):

    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1
    persons_query = f"""
        select "id", "c_deputy_no" from {db_config["target_schema"]}.persons
        where "type" = 'actor_deputy';
        """
    persons_df = pd.read_sql_query(persons_query, db_config["db_connection_string"])

    persons_df = persons_df[["id", "c_deputy_no"]]

    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )
    while True:
        try:

            phonenos_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            phonenos_joined_df = phonenos_df.merge(
                persons_df, how="left", left_on="c_deputy_no", right_on="c_deputy_no"
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

            target_db.insert_data(
                table_name=definition["destination_table_name"],
                df=phonenos_joined_df,
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
