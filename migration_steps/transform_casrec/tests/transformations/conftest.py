import pytest

from custom_logger import custom_logger
from utilities import transformations_from_mapping
import pandas as pd

logger = custom_logger(name="transformation_test")


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
        transformations_from_mapping, "add_unique_id", mock_add_unique_id
    )
