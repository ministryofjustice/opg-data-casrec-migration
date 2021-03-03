import json
import logging
import os

import psycopg2

log = logging.getLogger("root")

base_data_tables = ["assignees", "bond_providers"]


def empty_target_tables(db_config, db_engine, tables):
    tables_to_clear = tables

    tables_to_clear.reverse()
    tables_to_clear = tables_to_clear + base_data_tables

    for i, table in enumerate(tables_to_clear):
        log.debug(f"Clearing data from {table} in {db_config['target_schema']}")

        statement = f"""
        DELETE FROM {db_config['target_schema']}.{table} CASCADE;
        """

        try:
            db_engine.execute(statement)
        except Exception as e:
            log.error(
                f"There was an error clearing {table} in {db_config['target_schema']}"
            )
            log.debug(e)
            break
