import os
import sys
from pathlib import Path

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
def mock_get_lookup_dict_conditional(monkeypatch):
    def mock_lookup_dict(*args, **kwargs):
        print("using mock_get_lookup_dict_conditional")
        mock_lookup_dict = {
            "D": "Term Date",
        }
        return mock_lookup_dict

    monkeypatch.setattr(helpers, "get_lookup_dict", mock_lookup_dict)
