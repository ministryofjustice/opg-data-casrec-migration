import pandas as pd

from utilities.basic_data_table import get_basic_data_table

definition = {
    "source_table_name": "pat",
    "source_table_additional_columns": ["Case"],
    "destination_table_name": "phonenumbers",
}

mapping_file_name = "client_phonenumbers_mapping"


def insert_phonenumbers_clients(config, etl2_db):

    sirius_details, phonenos_df = get_basic_data_table(
        config=config, mapping_file_name=mapping_file_name, table_definition=definition
    )

    persons_query = (
        f'select "id", "caserecnumber" from etl2.persons '
        f"where \"type\" = 'actor_client';"
    )
    persons_df = pd.read_sql_query(persons_query, config.connection_string)

    persons_df = persons_df[["id", "caserecnumber"]]

    phonenos_joined_df = phonenos_df.merge(
        persons_df, how="left", left_on="c_case", right_on="caserecnumber"
    )

    phonenos_joined_df["person_id"] = phonenos_joined_df["id_y"]
    phonenos_joined_df = phonenos_joined_df.drop(columns=["id_y"])
    phonenos_joined_df = phonenos_joined_df.rename(columns={"id_x": "id"})

    etl2_db.insert_data(
        table_name=definition["destination_table_name"],
        df=phonenos_joined_df,
        sirius_details=sirius_details,
    )
