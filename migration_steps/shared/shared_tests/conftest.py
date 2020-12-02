import os
from pathlib import Path

import pytest
import sys

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")

import helpers


@pytest.fixture(autouse=True, scope="function")
def get_test_config(monkeypatch):
    def local_config():
        print("Using test config")

    monkeypatch.setattr(helpers, "get_config", local_config)


@pytest.fixture(autouse=True)
def mock_current_directory(monkeypatch):
    def mock_path():
        dirname = os.path.dirname(__file__)
        file_path = os.path.join(dirname, "mapping_defs/")
        return file_path

    monkeypatch.setattr(helpers, "get_current_directory", mock_path)
