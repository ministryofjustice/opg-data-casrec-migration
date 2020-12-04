import os

from pathlib import Path

import db_helpers

from load_to_target_helpers import get_cols_from_mapping

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sql_path = current_path / "../sql"


def target_update(config, conn_migration, conn_target):
    schema = config.schemas["integration"]
    persons_df = db_helpers.df_from_sql_file(
        sql_path, "get_skeleton_clients.sql", conn_migration, schema
    )
    columns = get_cols_from_mapping(
        file_name="client_persons_mapping",
        include_columns=["target_id", "salutation", "casesmanagedashybrid",],
        exclude_columns=["id", "sirius_id", "statusdate"],
        reorder_cols={"target_id": 0},
    )

    persons_df = persons_df[columns]

    persons_df = persons_df.rename(columns={"target_id": "id"})

    db_helpers.execute_update(
        conn=conn_target, df=persons_df, table="persons", pk_col="id"
    )


def target_add(config, conn_migration, conn_target):
    schema = config.schemas["integration"]
    persons_df = db_helpers.df_from_sql_file(
        sql_path, "get_new_clients.sql", conn_migration, schema
    )

    columns = get_cols_from_mapping(
        file_name="client_persons_mapping", exclude_columns=["id", "sirius_id"],
    )

    persons_df = persons_df[columns]
    # uid not implemented upstream so here's a workaround
    rowcount = len(persons_df.index)
    max_person_uid = db_helpers.result_from_sql_file(
        sql_path, "get_max_person_uid.sql", conn_target
    )
    persons_df["uid"] = list(
        range(max_person_uid + 1, max_person_uid + rowcount + 1, 1)
    )

    db_helpers.execute_insert(conn_target, persons_df, "persons")


def reindex_target_ids(config, conn_migration, conn_target):
    schema = config.schemas["integration"]
    sirius_persons_df = db_helpers.df_from_sql_file(
        sql_path, "select_sirius_clients.sql", conn_target
    )

    cursor = conn_migration.cursor()
    cursor.execute(f"TRUNCATE {schema}.sirius_map_clients;")
    conn_migration.commit()

    db_helpers.execute_insert(
        conn_migration, sirius_persons_df, f"{schema}.sirius_map_clients"
    )
