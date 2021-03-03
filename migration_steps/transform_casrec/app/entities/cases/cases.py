import pandas as pd
from utilities.basic_data_table import get_basic_data_table

definition = {
    "sheet_name": "cases",
    "source_table_name": "order",
    "source_table_additional_columns": ["Order No", "CoP Case", "Bond No."],
    "destination_table_name": "cases",
}
mapping_file_name = "cases_mapping"


def insert_cases(db_config, target_db):

    sirius_details, cases_df = get_basic_data_table(
        db_config=db_config,
        mapping_file_name=mapping_file_name,
        table_definition=definition,
    )

    persons_query = (
        f'select "id", "caserecnumber" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_client';"
    )
    persons_df = pd.read_sql_query(persons_query, db_config["db_connection_string"])

    persons_df = persons_df[["id", "caserecnumber"]]

    cases_joined_df = cases_df.merge(
        persons_df, how="left", left_on="caserecnumber", right_on="caserecnumber"
    )

    cases_joined_df["client_id"] = cases_joined_df["id_y"]
    cases_joined_df = cases_joined_df.drop(columns=["id_y"])
    cases_joined_df = cases_joined_df.rename(columns={"id_x": "id"})

    target_db.insert_data(
        table_name=definition["destination_table_name"],
        df=cases_joined_df,
        sirius_details=sirius_details,
    )
