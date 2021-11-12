import json
import logging
import os

import psycopg2

log = logging.getLogger("root")

base_data_tables = ["assignees", "bond_providers"]


def empty_target_tables(
    db_config, db_engine, tables, extra_tables=None, tables_copied_from_sirius=None
):
    if extra_tables:
        extra_table_list = [v["sirius_target_table"] for k, v in extra_tables.items()]
        tables_to_clear = extra_table_list + tables
    else:
        tables_to_clear = tables

    tables_to_clear.reverse()
    tables_to_clear = tables_to_clear + base_data_tables

    if tables_copied_from_sirius:
        tables_to_clear += list(tables_copied_from_sirius.keys())

    for i, table in enumerate(tables_to_clear):
        log.debug(f"Clearing data from {table} in {db_config['target_schema']}")

        statement = f"""
        DELETE FROM {db_config['target_schema']}.{table} CASCADE;
        """

        try:
            with db_engine.connect() as conn:
                conn.execute(statement)
        except Exception as e:
            log.error(
                f"There was an error clearing {table} in {db_config['target_schema']}"
            )
            log.debug(e)
            break
