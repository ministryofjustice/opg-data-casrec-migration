import pandas as pd
import psycopg2

"""
create and insert the persons table
"""
from transformations.single_data_table import all_steps

casrec_db_connection = psycopg2.connect(
    "host=localhost port=6666 "
    "dbname=casrecmigration "
    "user=casrec "
    "password=casrec"
)

definition = {
    "sheet_name": "addresses (Deputy)",
    "source_table_name": "deputy_address",
    "sirius_table_name": "addresses",
}


def final():
    addresses_df = all_steps(table_definition=definition)

    persons_query = f'select "id", "casrec_id" from etl2.persons;'
    persons_df = pd.read_sql_query(persons_query, casrec_db_connection)

    persons_df = persons_df[["id", "casrec_id"]]

    addresses_joined_df = addresses_df.merge(
        persons_df, how="left", left_on="casrec_id", right_on="casrec_id"
    )

    addresses_joined_df["person_id"] = addresses_joined_df["id_y"]
    addresses_joined_df = addresses_joined_df.drop(columns=["id_y"])
    addresses_joined_df = addresses_joined_df.rename(columns={"id_x": "id"})

    return addresses_joined_df
