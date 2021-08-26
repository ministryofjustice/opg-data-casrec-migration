import logging
import os


import pandas as pd

from utilities.db_helpers import (
    generate_select_query,
    update_ids,
    get_max_id_from_existing_table,
)
from utilities.generate_luhn_checksum import append_checksum

from table_helpers import check_enabled_by_table_name

log = logging.getLogger("root")

environment = os.environ.get("ENVIRONMENT")


MIN_NUMBER = 70000000000


def get_max_value_of_uid_sequence(db_connection_string, db_schema, table_names):

    max_values = []
    for table in table_names:
        max_uid = get_max_id_from_existing_table(
            db_connection_string=db_connection_string,
            db_schema=db_schema,
            table=table,
            id="uid",
        )
        if max_uid:
            max_values.append(max_uid)

        log.debug(f"max_uid: {max_uid} for table {table}")

    try:
        absolute_max_uid = max(max_values)
    except ValueError:
        absolute_max_uid = 0
    log.debug(f"absolute_max_uid: {absolute_max_uid}")

    return absolute_max_uid


def insert_unique_uids(db_config, target_db_engine):
    schema = db_config["target_schema"]
    # condition = {"method": "INSERT"}
    condition = {}
    source_columns = ["id", "uid"]
    all_table_names = ["persons", "cases"]

    enabled_tables = [
        x for x in all_table_names if check_enabled_by_table_name(table_name=x)
    ]

    sirius_max_uid = get_max_value_of_uid_sequence(
        db_connection_string=db_config["sirius_db_connection_string"],
        db_schema=db_config["sirius_schema"],
        table_names=enabled_tables,
    )
    try:
        sirius_max_seq_val = int(str(sirius_max_uid)[:-1]) - MIN_NUMBER
    except ValueError:
        sirius_max_seq_val = 0

    for table in enabled_tables:
        log.info(f"table: {table}")
        initial_target_max_uid = get_max_value_of_uid_sequence(
            db_connection_string=db_config["db_connection_string"],
            db_schema=db_config["target_schema"],
            table_names=enabled_tables,
        )
        try:
            target_max_seq_val = int(str(initial_target_max_uid)[:-1]) - MIN_NUMBER
        except ValueError:
            target_max_seq_val = 0

        uid_seq_starting_value = max([sirius_max_seq_val, target_max_seq_val]) + 1
        uid_starting_value = uid_seq_starting_value + MIN_NUMBER

        source_data_query = generate_select_query(
            schema=schema, table=table, columns=source_columns, where_clause=condition
        )
        log.debug(f"Getting source data using query {source_data_query}")

        source_data_df = pd.read_sql_query(con=target_db_engine, sql=source_data_query)

        source_data_df.insert(
            0,
            "uid_no_checksum",
            range(uid_starting_value, uid_starting_value + len(source_data_df)),
        )

        source_data_df["uid"] = source_data_df["uid_no_checksum"].apply(
            lambda x: append_checksum(x)
        )
        source_data_df = source_data_df.drop(columns="uid_no_checksum")

        rows_to_update = zip(source_data_df["id"], source_data_df["uid"])

        log.debug("Now update the table....")
        update_ids(
            db_connection_string=db_config["db_connection_string"],
            db_schema=db_config["target_schema"],
            table=table,
            column_name="uid",
            update_data=rows_to_update,
        )
