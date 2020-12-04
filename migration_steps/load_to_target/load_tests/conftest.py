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
import helpers

logger = logging.getLogger("tests")
logger.addHandler(custom_logger.MyHandler())
logger.setLevel("INFO")


@pytest.fixture
def test_config():
    config = config2.get_config(env="local")
    return config


@pytest.fixture()
def mock_persons_df(monkeypatch, request):
    def mock_persons(*args, **kwargs):
        print("using mock_df_from_sql_file")

        dirname = os.path.dirname(__file__)
        test_file = os.path.join(dirname, "test_data", "persons_df.json")
        with open(test_file, "r") as test_json:
            test_data_raw = test_json.read()
            test_source_data_dict = json.loads(test_data_raw)

        test_source_data_df = pd.DataFrame(
            test_source_data_dict, columns=[x for x in test_source_data_dict]
        )

        return test_source_data_df

    monkeypatch.setattr(db_helpers, "df_from_sql_file", mock_persons)


@pytest.fixture()
def mock_execute_update_with_logs(monkeypatch):
    def execute_update(conn, df, table, pk_col):
        print("using mock_execute_update")

        cols = list(df.columns)

        logger.info(f"cols: {cols}")
        logger.info(f"pk_col: {pk_col}")

    monkeypatch.setattr(db_helpers, "execute_update", execute_update)


@pytest.fixture()
def mock_execute_insert_with_logs(monkeypatch):
    def execute_insert(conn, df, table):
        print("using mock_execute_insert")

        tuples = [tuple(x) for x in df.to_numpy()]
        cols = ",".join(list(df.columns))

        logger.info(f"cols: {cols}")
        logger.info(f"tuples: {tuples}")

    monkeypatch.setattr(db_helpers, "execute_insert", execute_insert)


@pytest.fixture()
def mock_result_from_sql_file(monkeypatch):
    def result_from_sql_file(*args, **kwargs):
        return 1

    monkeypatch.setattr(db_helpers, "result_from_sql_file", result_from_sql_file)


@pytest.fixture()
def mock_get_mapping_dict(monkeypatch):
    def get_mapping_dict(*args, **kwargs):
        print("using mock_get_mapping_dict")

        dirname = os.path.dirname(__file__)
        test_file = os.path.join(
            dirname, "test_data", "test_client_persons_sirius_data.json"
        )
        with open(test_file, "r") as test_json:
            test_data_raw = test_json.read()
            return json.loads(test_data_raw)

    monkeypatch.setattr(helpers, "get_mapping_dict", get_mapping_dict)
