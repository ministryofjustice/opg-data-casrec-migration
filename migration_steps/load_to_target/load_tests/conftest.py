import logging
import os
from pathlib import Path

import pandas as pd
import pytest
import sys

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")
# current_path = Path(os.path.dirname(os.path.realpath(__file__)))
# sys.path.insert(0, str(current_path) + "/../migration_steps/shared")


import custom_logger
import json
import config2
import db_helpers

logger = logging.getLogger("tests")
logger.addHandler(custom_logger.MyHandler())
logger.setLevel("INFO")


@pytest.fixture
def test_config():
    config = config2.get_config(env="local")
    return config


@pytest.fixture()
def mock_df_from_sql_file(monkeypatch):
    def mock_persons_df(*args, **kwargs):
        print("using mock_df_from_sql_file")

        dirname = os.path.dirname(__file__)
        test_file = os.path.join(dirname, "test_dataframes", "persons_df.json")
        with open(test_file, "r") as test_json:
            test_data_raw = test_json.read()
            test_source_data_dict = json.loads(test_data_raw)

        test_source_data_df = pd.DataFrame(
            test_source_data_dict, columns=[x for x in test_source_data_dict]
        )

        return test_source_data_df

    monkeypatch.setattr(db_helpers, "df_from_sql_file", mock_persons_df)


@pytest.fixture()
def mock_execute_update(monkeypatch):
    def execute_update(conn, df, table):
        print("using mock_execute_update")

        cols = list(df.columns)
        pk_col = cols.pop(0)
        colstring = "=%s,".join(cols)
        colstring += "=%s"
        update_template = f"UPDATE {table} SET {colstring} WHERE {pk_col}="

        logger.info(f"cols: {cols}")
        logger.info(f"pk_col: {pk_col}")
        logger.info(f"colstring: {colstring}")
        logger.info(f"colstring: {colstring}")
        logger.info(f"update_template: {update_template}")

    monkeypatch.setattr(db_helpers, "execute_update", execute_update)
