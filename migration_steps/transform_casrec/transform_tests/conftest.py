import pytest
import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")

import helpers


@pytest.fixture(autouse=True, scope="function")
def get_test_config(monkeypatch):
    def local_config():
        print("Using test config")
        # return LocalConfig()

    monkeypatch.setattr(helpers, "get_config", local_config)
