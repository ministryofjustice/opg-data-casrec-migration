import logging
import os

import pandas as pd

import helpers

from transform_data.apply_datatypes import apply_datatypes
from utilities.convert_json_to_mappings import MappingDefinitions

from transform_data import calculations as process_calculations
from transform_data import default_columns as process_default_columns
from transform_data import lookup_tables as process_lookup_tables
from transform_data import simple_mappings as process_simple_mappings
from transform_data import simple_transformations as process_simple_transformations
from transform_data import unique_id as process_unique_id

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


def perform_transformations(
    mapping_definitions: dict,
    table_definition: dict,
    source_data_df: pd.DataFrame,
    db_conn_string: str,
    db_schema: str,
    sirius_details: dict = None,
) -> pd.DataFrame:

    mapping_defs = MappingDefinitions(mapping_definitions=mapping_definitions)
    mappings = mapping_defs.generate_mapping_def()

    final_df = source_data_df

    log.log(
        config.DATA,
        f"Data before transformations\n{final_df.sample(n=config.row_limit).to_markdown()}",
    )

    simple_mapping = mappings["simple_mapping"]
    transformations = mappings["transformations"]
    required_columns = mappings["required_columns"]
    calculated_fields = mappings["calculated_fields"]
    lookup_tables = mappings["lookup_tables"]

    if len(simple_mapping) > 0:
        final_df = process_simple_mappings.do_simple_mapping(
            simple_mapping, table_definition, final_df
        )

    if len(transformations) > 0:
        final_df = process_simple_transformations.do_simple_transformations(
            transformations, final_df
        )

    if len(required_columns) > 0:
        final_df = process_default_columns.add_required_columns(
            required_columns, final_df
        )

    if len(calculated_fields) > 0:
        final_df = process_calculations.do_calculations(calculated_fields, final_df)

    if len(lookup_tables) > 0:
        final_df = process_lookup_tables.map_lookup_tables(lookup_tables, final_df)

    if "id" not in source_data_df.columns.values.tolist():
        final_df = process_unique_id.add_unique_id(
            db_conn_string, db_schema, table_definition, final_df
        )

    if sirius_details:
        final_df = apply_datatypes(mapping_details=sirius_details, df=final_df)

    log.log(
        config.DATA,
        f"Data after transformations\n{final_df.sample(n=config.row_limit).to_markdown()}",
    )

    return final_df
