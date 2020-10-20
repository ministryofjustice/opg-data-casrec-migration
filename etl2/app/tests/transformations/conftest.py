import pytest

from logger import custom_logger
from transformations import transformations_from_mapping
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
def mock_max_id_from_db(monkeypatch):
    def mock_df(query, db_conn):
        return pd.DataFrame([55], columns=["max"])

    monkeypatch.setattr(pd, "read_sql_query", mock_df)
