import os

from pathlib import Path

import db_helpers

import helpers

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sql_path = current_path / "../sql"


def get_cols_from_mapping(df, file_name, first_column=None):

    sirius_data = helpers.get_mapping_dict(
        file_name=file_name, stage_name="sirius_details", only_complete_fields=True,
    )
    cols_from_mapping = list(sirius_data.keys())
    include_columns = ["target_id"]
    exclude_columns = ["id", "sirius_id"]

    columns_to_select = [
        x for x in cols_from_mapping if x not in exclude_columns
    ] + include_columns

    if first_column:
        columns_to_select.insert(
            0, columns_to_select.pop(columns_to_select.index(first_column))
        )

    df = df[columns_to_select]

    return df


def target_update(config, conn_migration, conn_target):
    schema = config.schemas["integration"]
    persons_df = db_helpers.df_from_sql_file(
        sql_path, "get_skeleton_clients.sql", conn_migration, schema
    )
    persons_df = get_cols_from_mapping(
        df=persons_df, file_name="client_persons_mapping"
    )

    persons_df = persons_df.rename(columns={"target_id": "id"})

    persons_df = persons_df.set_index("id")

    db_helpers.execute_update(conn_target, persons_df, "persons")


def target_add(config, conn_migration, conn_target):
    schema = config.schemas["integration"]
    persons_df = db_helpers.df_from_sql_file(
        sql_path, "get_new_clients.sql", conn_migration, schema
    )
    persons_df = get_cols_from_mapping(
        df=persons_df, file_name="client_persons_mapping", first_column="target_id"
    )

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
