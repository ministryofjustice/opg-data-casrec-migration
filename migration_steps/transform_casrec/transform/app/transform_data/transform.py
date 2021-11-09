import logging
import os

import pandas as pd

import helpers
from custom_errors import EmptyDataFrame
from decorators import timer
from transform_data.apply_conditions import source_conditions

from transform_data.apply_datatypes import apply_datatypes
from utilities.convert_json_to_mappings import MappingDefinitions

from transform_data import calculations as process_calculations
from transform_data import default_columns as process_default_columns
from transform_data import lookup_tables as process_lookup_tables
from transform_data import simple_mappings as process_simple_mappings
from transform_data import simple_transformations as process_simple_transformations
from transform_data import unique_id as process_unique_id
from transform_data.table_transforms import process_table_transformations


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

    conditions = table_definition.get("source_conditions")
    table_transforms = table_definition.get("table_transforms")

    simple_mapping = mappings["simple_mapping"]
    transformations = mappings["transformations"]
    required_columns = mappings["required_columns"]
    calculated_fields = mappings["calculated_fields"]
    lookup_tables = mappings["lookup_tables"]

    if conditions:
        log.debug("Applying conditions to source data")
        final_df = source_conditions(df=final_df, conditions=dict(conditions))
        if len(final_df) == 0:
            log.debug(f"No data left after applying source conditions")
            raise EmptyDataFrame(empty_data_frame_type="chunk with conditions applied")

    if len(simple_mapping) > 0:
        log.debug("Applying simple mappings")
        final_df = process_simple_mappings.do_simple_mapping(
            simple_mapping, table_definition, final_df
        )
        if len(final_df) == 0:
            log.debug(f"No data left after simple_mapping")
            raise EmptyDataFrame(
                empty_data_frame_type="chunk with simple mappings applied"
            )

    if len(transformations) > 0:
        log.debug("Applying transformations")
        final_df = process_simple_transformations.do_simple_transformations(
            transformations, final_df
        )
        if len(final_df) == 0:
            log.debug(f"No data left after transformations")
            raise EmptyDataFrame(
                empty_data_frame_type="chunk with simple transformations applied"
            )

    if len(required_columns) > 0:
        log.debug("Applying default columns")
        final_df = process_default_columns.add_required_columns(
            required_columns, final_df
        )
        if len(final_df) == 0:
            log.debug(f"No data left after default columns")
            raise EmptyDataFrame(
                empty_data_frame_type="chunk with required columns applied"
            )

    if len(calculated_fields) > 0:
        log.debug("Applying calculated fields")
        final_df = process_calculations.do_calculations(calculated_fields, final_df)

        if len(final_df) == 0:
            log.debug(f"No data left after calculated fields")
            raise EmptyDataFrame(
                empty_data_frame_type="chunk with calculations applied"
            )

    if len(lookup_tables) > 0:
        log.debug("Applying lookup tables")
        final_df = process_lookup_tables.map_lookup_tables(lookup_tables, final_df)

        if len(final_df) == 0:
            log.debug(f"No data left after lookup tables")
            raise EmptyDataFrame(empty_data_frame_type="chunk with lookups applied")

    if table_transforms:
        log.debug("Applying table transformations")
        final_df = process_table_transformations(df=final_df, transforms_for_table=table_transforms)
        if len(final_df) == 0:
            log.debug(f"No data left after table transformations")
            raise EmptyDataFrame(empty_data_frame_type="chunk with table transformations applied")

    if "id" not in source_data_df.columns.values.tolist():
        log.debug("Applying unique id")
        final_df = process_unique_id.add_unique_id(
            db_conn_string, db_schema, table_definition, final_df
        )
        if len(final_df) == 0:
            raise EmptyDataFrame(empty_data_frame_type="chunk with unique IDs applied")

    if sirius_details:
        log.debug("Applying datatypes")
        final_df = apply_datatypes(mapping_details=sirius_details, df=final_df)
        if len(final_df) == 0:
            raise EmptyDataFrame(empty_data_frame_type="chunk with datatypes applied")

    return final_df
