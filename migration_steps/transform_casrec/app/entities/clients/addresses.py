import pandas as pd
from utilities.basic_data_table import get_basic_data_table

definition = {
    "source_table_name": "pat",
    "source_table_additional_columns": ["Case"],
    "destination_table_name": "addresses",
}
mapping_file_name = "client_addresses_mapping"


def insert_addresses_clients(db_config, target_db):

    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1
    persons_query = (
        f'select "id", "caserecnumber" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_client';"
    )
    persons_df = pd.read_sql_query(persons_query, db_config["db_connection_string"])

    persons_df = persons_df[["id", "caserecnumber"]]

    while True:
        try:
            sirius_details, addresses_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=definition,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            addresses_joined_df = addresses_df.merge(
                persons_df, how="left", left_on="c_case", right_on="caserecnumber"
            )

            addresses_joined_df["person_id"] = addresses_joined_df["id_y"]
            addresses_joined_df = addresses_joined_df.drop(columns=["id_y"])
            addresses_joined_df = addresses_joined_df.rename(columns={"id_x": "id"})

            target_db.insert_data(
                table_name=definition["destination_table_name"],
                df=addresses_joined_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

            offset += chunk_size
            chunk_no += 1

        except Exception:
            break
