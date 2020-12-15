import os
from db_helpers import (
    result_from_sql_file,
    df_from_sql_file,
    execute_insert,
    execute_sql_file,
)
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sql_path = current_path / "../sql"


def load_fixtures(config, conn_migration, conn_target):
    schema = config.schemas["integration"]
    max_person_uid = result_from_sql_file(
        sql_path, "get_max_person_uid.sql", conn_target
    )
    persons_df = df_from_sql_file(
        sql_path, "fixtures_select_clients.sql", conn_migration, schema
    )
    persons_df["uid"] = list(range(max_person_uid + 1, max_person_uid + 11, 1))
    execute_insert(conn_target, persons_df, "persons")


def fetch_target_ids(config, conn_migration, conn_target):
    schema = config.schemas["integration"]
    sirius_persons_df = df_from_sql_file(
        sql_path, "select_sirius_clients.sql", conn_target
    )
    execute_insert(
        conn_migration, sirius_persons_df, f"{schema}.sirius_map_client_persons"
    )


def merge_target_ids(config, conn_migration, conn_target):
    schema = config.schemas["integration"]
    execute_sql_file(sql_path, "merge_target_clients.sql", conn_migration, schema)
