import logging
import custom_logger
import pytest
import transform_data

# from transform_data import simple_mappings, simple_transformations, default_columns, unique_id

logger = logging.getLogger("tests")
logger.addHandler(custom_logger.MyHandler())
logger.setLevel("INFO")


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
        print("using mock_map_lookup_tables")
        logger.info("mock map_lookup_tables")
        return df

    def mock_add_unique_id(db_conn_string, db_schema, table_definition, df):
        logger.info("mock add_unique_id")
        return df

    monkeypatch.setattr(
        transform_data.simple_mappings, "do_simple_mapping", mock_do_simple_mapping
    )
    monkeypatch.setattr(
        transform_data.simple_transformations,
        "do_simple_transformations",
        mock_do_simple_transformations,
    )
    monkeypatch.setattr(
        transform_data.default_columns,
        "add_required_columns",
        mock_add_required_columns,
    )
    monkeypatch.setattr(
        transform_data.lookup_tables, "map_lookup_tables", mock_map_lookup_tables
    )
    monkeypatch.setattr(transform_data.unique_id, "add_unique_id", mock_add_unique_id)
