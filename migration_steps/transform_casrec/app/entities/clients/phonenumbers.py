import json

import pandas as pd

from utilities import transformations_from_mapping
from utilities.generate_source_query import generate_select_string_from_mapping
from utilities.helpers import get_mapping_file

definition = {
    "source_table_name": "pat",
    "source_table_additional_columns": ["Case"],
    "destination_table_name": "phonenumbers",
}


def insert_phonenumbers_clients(config, etl2_db):

    with open(
        get_mapping_file(file_name="client_phonenumbers_mapping")
    ) as mapping_json:
        mapping_dict = json.load(mapping_json)

    source_data_query = generate_select_string_from_mapping(
        mapping=mapping_dict,
        source_table_name=definition["source_table_name"],
        additional_columns=definition["source_table_additional_columns"],
        db_schema=config.etl1_schema,
    )

    source_data_df = pd.read_sql_query(
        sql=source_data_query, con=config.connection_string
    )

    phonenos_df = transformations_from_mapping.perform_transformations(
        mapping_dict,
        definition,
        source_data_df,
        config.connection_string,
        config.etl2_schema,
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
        table_name=definition["destination_table_name"], df=phonenos_joined_df
    )
