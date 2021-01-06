import pandas as pd

from utilities.basic_data_table import get_basic_data_table

definition = {
    "sheet_name": "addresses (Client)",
    "source_table_name": "pat",
    "source_table_additional_columns": ["Case"],
    "destination_table_name": "addresses",
}
mapping_file_name = "client_addresses_mapping"


def insert_addresses_clients(config, etl2_db):

    sirius_details, addresses_df = get_basic_data_table(
        config=config, mapping_file_name=mapping_file_name, table_definition=definition
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
        table_name=definition["destination_table_name"],
        df=addresses_joined_df,
        sirius_details=sirius_details,
    )
