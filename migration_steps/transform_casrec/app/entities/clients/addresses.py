import pandas as pd
from utilities import transformations_from_mapping
from utilities.generate_source_query import generate_select_string_from_mapping
from utilities.helpers import get_mapping_dict

definition = {
    "sheet_name": "addresses (Client)",
    "source_table_name": "pat",
    "source_table_additional_columns": ["Case"],
    "destination_table_name": "addresses",
}


def insert_addresses_clients(config, etl2_db):

    mapping_dict = get_mapping_dict(file_name="client_addresses_mapping")

    source_data_query = generate_select_string_from_mapping(
        mapping=mapping_dict,
        source_table_name=definition["source_table_name"],
        additional_columns=definition["source_table_additional_columns"],
        db_schema=config.etl1_schema,
    )

    source_data_df = pd.read_sql_query(
        sql=source_data_query, con=config.connection_string
    )

    addresses_df = transformations_from_mapping.perform_transformations(
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

    addresses_joined_df = addresses_df.merge(
        persons_df, how="left", left_on="c_case", right_on="caserecnumber"
    )

    addresses_joined_df["person_id"] = addresses_joined_df["id_y"]
    addresses_joined_df = addresses_joined_df.drop(columns=["id_y"])
    addresses_joined_df = addresses_joined_df.rename(columns={"id_x": "id"})

    etl2_db.insert_data(
        table_name=definition["destination_table_name"], df=addresses_joined_df
    )
