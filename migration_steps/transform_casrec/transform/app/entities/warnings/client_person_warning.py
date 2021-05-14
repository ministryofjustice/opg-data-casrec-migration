import pandas as pd

from helpers import get_mapping_dict


definition = {
    "destination_table_name": "person_warning",
    "source_table_name": "",
    "source_table_additional_columns": [],
}

mapping_file_name = "person_warning_mapping"


def insert_client_person_warning(db_config, target_db):

    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    clients_query = (
        f'select "id", "caserecnumber" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_client';"
    )
    clients_df = pd.read_sql_query(clients_query, db_config["db_connection_string"])

    client_warning_query = (
        f'select "id", "c_case" from {db_config["target_schema"]}.warnings;'
    )
    client_warning_df = pd.read_sql_query(
        client_warning_query, db_config["db_connection_string"]
    )

    client_warning_df = client_warning_df.merge(
        clients_df,
        how="left",
        left_on="c_case",
        right_on="caserecnumber",
        suffixes=["_warning", "_client"],
    )

    client_warning_df = client_warning_df.drop(columns=["caserecnumber"])
    client_warning_df = client_warning_df.rename(
        columns={"id_warning": "warning_id", "id_client": "person_id"}
    )
    client_warning_df["casrec_details"] = None

    target_db.insert_data(
        table_name=definition["destination_table_name"],
        df=client_warning_df,
        sirius_details=sirius_details,
    )