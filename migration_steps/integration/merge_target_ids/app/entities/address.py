import os
from db_helpers import execute_insert, df_from_sql_file, execute_sql_file
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sql_path = current_path / "../sql"


def load_fixtures(self, conn_target):
    execute_sql_file(sql_path, "fixtures_add_addresses.sql", conn_target)


def fetch_target_ids(config, conn_migration, conn_target):
    schema = config.schemas["integration"]
    sirius_addresses_df = df_from_sql_file(
        sql_path, "select_sirius_addresses.sql", conn_target
    )
    execute_insert(
        conn_migration, sirius_addresses_df, f"{schema}.sirius_map_client_addresses"
    )


def merge_target_ids(config, conn_migration, conn_target):
    schema = config.schemas["integration"]
    execute_sql_file(sql_path, "merge_target_addresses.sql", conn_migration, schema)
