import pandas as pd

from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols


def get_client_person_warning_records(
    db_config,
    mapping_file_name,
    table_definition,
    sirius_details,
    chunk_size,
    offset,
    prep
):
    client_warning_query = f'select * from {db_config["target_schema"]}.warnings;'

    client_warning_df = pd.read_sql_query(
        client_warning_query, db_config["db_connection_string"]
    )

    if len(client_warning_df) == 0:
        return (client_warning_df, False)

    clients_query = (
        f'select "id", "caserecnumber" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_client';"
    )

    clients_df = pd.read_sql_query(clients_query, db_config["db_connection_string"])

    client_warning_df = client_warning_df[["id", "c_case"]]

    client_warning_df = client_warning_df.merge(
        clients_df,
        how="inner",
        left_on="c_case",
        right_on="caserecnumber",
        suffixes=["_warning", "_client"],
    )

    client_warning_df = client_warning_df.drop(columns=["caserecnumber"])

    client_warning_df = client_warning_df.rename(
        columns={"id_warning": "warning_id", "id_client": "person_id"}
    )

    client_warning_df["casrec_details"] = "{}"

    client_warning_df = reapply_datatypes_to_fk_cols(
        columns=["person_id", "warning_id"], df=client_warning_df
    )

    return (client_warning_df, False)
