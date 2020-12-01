import os
from db_helpers import (
    df_from_sql_file,
    execute_update,
    result_from_sql_file,
    execute_insert,
)
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sql_path = current_path / "../sql"


def target_update(config, conn_migration, conn_target):
    schema = config.schemas["integration"]
    persons_df = df_from_sql_file(
        sql_path, "get_skeleton_clients.sql", conn_migration, schema
    )

    # transpose id column
    persons_df = persons_df.drop(["id", "sirius_id"], axis=1)
    persons_df = persons_df.rename(columns={"target_id": "id"})

    # these columns not implemented upstream yet so drop them for now
    persons_df = persons_df.drop(
        ["statusdate", "updateddate", "dateofdeath", "c_term_type"], axis=1
    )

    execute_update(conn_target, persons_df, "persons")


def target_add(config, conn_migration, conn_target):
    schema = config.schemas["integration"]
    persons_df = df_from_sql_file(
        sql_path, "get_new_clients.sql", conn_migration, schema
    )

    # don't send id
    persons_df = persons_df.drop(["id", "sirius_id"], axis=1)
    persons_df["clientsource"] = "CASRECMIGRATION"

    # these columns not implemented upstream yet so drop them for now
    persons_df = persons_df.drop(
        ["statusdate", "updateddate", "dateofdeath", "c_term_type"], axis=1
    )

    # uid not implemented upstream so here's a workaround
    rowcount = len(persons_df.index)
    max_person_uid = result_from_sql_file(
        sql_path, "get_max_person_uid.sql", conn_target
    )
    persons_df["uid"] = list(
        range(max_person_uid + 1, max_person_uid + rowcount + 1, 1)
    )

    execute_insert(conn_target, persons_df, "persons")


def reindex_target_ids(config, conn_migration, conn_target):
    schema = config.schemas["integration"]
    sirius_persons_df = df_from_sql_file(
        sql_path, "select_sirius_clients.sql", conn_target
    )

    cursor = conn_migration.cursor()
    cursor.execute(f"TRUNCATE {schema}.sirius_map_clients;")
    conn_migration.commit()

    execute_insert(conn_migration, sirius_persons_df, f"{schema}.sirius_map_clients")
