import json
import os
import db_helpers
from pathlib import Path

from load_to_target_helpers import get_cols_from_mapping

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sql_path = current_path / "../sql"


def target_update(config, conn_migration, conn_target):
    schema = config.schemas["integration"]
    addresses_df = db_helpers.df_from_sql_file(
        sql_path, "get_skeleton_addresses.sql", conn_migration, schema
    )

    columns = get_cols_from_mapping(
        file_name="client_addresses_mapping",
        include_columns=["target_id"],
        exclude_columns=["id", "sirius_id", "person_id", "c_case", "caserecnumber"],
        reorder_cols={"target_id": 0},
    )

    addresses_df = addresses_df[columns]

    addresses_df = addresses_df.rename(
        columns={"target_id": "id", "sirius_person_id": "person_id"}
    )

    # This will not be needed once the datatype fix is complete
    # addresses_df["isairmailrequired"] = addresses_df["isairmailrequired"].replace(
    #     {"True": True, "False": False}
    # )

    addresses_df["address_lines"] = addresses_df["address_lines"].apply(json.dumps)

    db_helpers.execute_update(
        conn=conn_target, df=addresses_df, table="addresses", pk_col="id"
    )


def target_add(config, conn_migration, conn_target):
    schema = config.schemas["integration"]
    addresses_df = db_helpers.df_from_sql_file(
        sql_path, "get_new_addresses.sql", conn_migration, schema
    )

    columns = get_cols_from_mapping(
        file_name="client_addresses_mapping",
        exclude_columns=["id", "sirius_id", "person_id", "c_case", "caserecnumber"],
    )

    addresses_df = addresses_df[columns]

    addresses_df = addresses_df.rename(columns={"sirius_person_id": "person_id"})

    addresses_df["address_lines"] = addresses_df["address_lines"].apply(json.dumps)

    # This will not be needed once the datatype fix is complete
    # addresses_df["isairmailrequired"] = addresses_df["isairmailrequired"].replace(
    #     {"True": True, "False": False}
    # )

    db_helpers.execute_insert(conn_target, addresses_df, "addresses")


def reindex_target_ids(config, conn_migration):
    schema = config.schemas["integration"]
    db_helpers.execute_sql_file(
        sql_path, "merge_target_addresses.sql", conn_migration, schema
    )
