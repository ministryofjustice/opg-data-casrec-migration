import os
import sys
from pathlib import Path

import utilities

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import logging
import pytest
import custom_logger

logger = logging.getLogger("tests")
logger.addHandler(custom_logger.MyHandler())
logger.setLevel("INFO")


@pytest.fixture()
def mock_calculations(monkeypatch):
    def mock_current_date(column_name, df):
        print("using mock_current_date")
        logger.info("mock current_date")
        return df

    # def mock_conditional_lookup(column_name, lookup_file_name, df):
    #     logger.info("mock conditional_lookup")
    #     return df

    monkeypatch.setattr(
        utilities.standard_calculations, "current_date", mock_current_date
    )
    # monkeypatch.setattr(
    #     calculated_fields, "conditional_lookup", mock_conditional_lookup
    # )
