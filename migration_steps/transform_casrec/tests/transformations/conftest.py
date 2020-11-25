import sys
import os
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import logging
import pytest
import custom_logger
import helpers
from utilities import transformations_from_mapping


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

    def mock_date_format_standard(original_cols, final_cols, df):
        logger.info("mock date_format_standard")
        return df

    def mock_unique_number(final_cols, df):
        logger.info("mock unique_number")
        return df

    def mock_capitalise(original_col, final_col, df):
        logger.info("mock capitalise")
        return df

    monkeypatch.setattr(
        transformations_from_mapping, "squash_columns", mock_squash_columns
    )
    monkeypatch.setattr(
        transformations_from_mapping, "convert_to_bool", mock_convert_to_bool
    )
    monkeypatch.setattr(
        transformations_from_mapping, "date_format_standard", mock_date_format_standard
    )
    monkeypatch.setattr(
        transformations_from_mapping, "unique_number", mock_unique_number
    )
    monkeypatch.setattr(transformations_from_mapping, "capitalise", mock_capitalise)


@pytest.fixture()
def mock_calculations(monkeypatch):
    def mock_current_date(column_name, df):
        logger.info("mock current_date")
        return df

    monkeypatch.setattr(transformations_from_mapping, "current_date", mock_current_date)


@pytest.fixture()
def mock_transformation_steps(monkeypatch):
    def mock_do_simple_mapping(mapping, table_defs, df):
        logger.info("mock do_simple_mapping")
        return df

    def mock_do_simple_transformations(mapping, df):
        logger.info("mock do_simple_transformations")
        return df

    def mock_add_required_columns(mapping, df):
        logger.info("mock add_required_columns")
        return df

    def mock_map_lookup_tables(mapping, df):
        logger.info("mock map_lookup_tables")
        return df

    def mock_add_unique_id(db_conn_string, db_schema, table_definition, df):
        logger.info("mock add_unique_id")
        return df

    monkeypatch.setattr(
        transformations_from_mapping, "do_simple_mapping", mock_do_simple_mapping
    )
    monkeypatch.setattr(
        transformations_from_mapping,
        "do_simple_transformations",
        mock_do_simple_transformations,
    )
    monkeypatch.setattr(
        transformations_from_mapping, "add_required_columns", mock_add_required_columns
    )
    monkeypatch.setattr(
        transformations_from_mapping, "map_lookup_tables", mock_map_lookup_tables
    )
    monkeypatch.setattr(
        transformations_from_mapping, "add_unique_id", mock_add_unique_id
    )


@pytest.fixture()
def mock_get_lookup_dict(monkeypatch):
    def mock_lookup_dict(*args, **kwargs):
        print("using mock_lookup_dict")
        mock_lookup_dict = {"1": "Miss", "2": "Ms", "3": "Mr", "4": "Sir"}
        return mock_lookup_dict

    monkeypatch.setattr(helpers, "get_lookup_dict", mock_lookup_dict)
