import sys
import os
from pathlib import Path

import utilities

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import logging
import pytest
import custom_logger
import helpers


logger = logging.getLogger("tests")
logger.addHandler(custom_logger.MyHandler())
logger.setLevel("INFO")


@pytest.fixture()
def mock_standard_transformations(monkeypatch):
    def mock_squash_columns(original_cols, final_cols, df):
        logger.info("mock squash_columns")
        return df

    def mock_convert_to_bool(original_cols, final_cols, df):
        logger.info("mock convert_to_bool")
        return df

    def mock_unique_number(final_cols, df):
        logger.info("mock unique_number")
        return df

    def mock_capitalise(original_col, final_col, df):
        logger.info("mock capitalise")
        return df

    monkeypatch.setattr(
        utilities.standard_transformations, "squash_columns", mock_squash_columns
    )
    monkeypatch.setattr(
        utilities.standard_transformations, "convert_to_bool", mock_convert_to_bool
    )

    monkeypatch.setattr(
        utilities.standard_transformations, "unique_number", mock_unique_number
    )
    monkeypatch.setattr(
        utilities.standard_transformations, "capitalise", mock_capitalise
    )
