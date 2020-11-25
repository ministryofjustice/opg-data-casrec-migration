import logging
import os

import pandas as pd

from config import get_config
import helpers
from utilities.calculated_fields import current_date
from utilities.standard_transformations import (
    unique_number,
    squash_columns,
    convert_to_bool,
    date_format_standard,
    capitalise,
)

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = get_config(env=environment)


def do_simple_mapping(
    simple_mapping: dict, table_definition: dict, source_data_df: pd.DataFrame
) -> pd.DataFrame:

    log.log(config.VERBOSE, "starting to apply simple mapping")
    log.log(config.VERBOSE, f"simple mapping dict: {simple_mapping}")

    source_table_name = table_definition["source_table_name"]

    simple_column_remap = [
        {v["alias"]: k}
        for k, v in simple_mapping.items()
        if v["requires_transformation"] == ""
        and v["casrec_table"].lower() == source_table_name
    ]
    columns = {k: v for d in simple_column_remap for k, v in d.items()}

    return source_data_df.rename(columns=columns)


def do_simple_transformations(
    transformations: dict, source_data_df: pd.DataFrame
) -> pd.DataFrame:
    log.log(config.VERBOSE, "starting to apply transformations")
    transformed_df = source_data_df

    if "squash_columns" in transformations:
        for t in transformations["squash_columns"]:
            transformed_df = squash_columns(
                t["original_columns"], t["aggregate_col"], transformed_df
            )
    if "convert_to_bool" in transformations:
        for t in transformations["convert_to_bool"]:
            transformed_df = convert_to_bool(
                t["original_columns"], t["aggregate_col"], transformed_df
            )
    if "date_format_standard" in transformations:
        for t in transformations["date_format_standard"]:
            transformed_df = date_format_standard(
                t["original_columns"], t["aggregate_col"], transformed_df
            )
    if "unique_number" in transformations:
        for t in transformations["unique_number"]:
            transformed_df = unique_number(t["aggregate_col"], transformed_df)

    if "capitalise" in transformations:
        for t in transformations["capitalise"]:
            transformed_df = capitalise(
                t["original_columns"], t["aggregate_col"], transformed_df
            )

    return transformed_df


def do_calculations(
    calculated_fields: dict, source_data_df: pd.DataFrame
) -> pd.DataFrame:
    log.log(config.VERBOSE, "starting to apply calculations")
    calculations_df = source_data_df

    if "current_date" in calculated_fields:
        for t in calculated_fields["current_date"]:
            calculations_df = current_date(t["column_name"], calculations_df)

    return calculations_df


def add_required_columns(
    required_columns: dict, source_data_df: pd.DataFrame
) -> pd.DataFrame:
    log.log(config.VERBOSE, "starting to apply required columns")
    for col, details in required_columns.items():
        source_data_df[col] = details["default_value"]

    return source_data_df


def map_lookup_tables(
    lookup_tables: dict, source_data_df: pd.DataFrame
) -> pd.DataFrame:

    for col, details in lookup_tables.items():
        lookup_dict = helpers.get_lookup_dict(file_name=details["lookup_table"])

        source_data_df[col] = source_data_df[col].map(lookup_dict)

        source_data_df[col] = source_data_df[col].fillna("")

    return source_data_df


def add_unique_id(
    db_conn_string: str,
    db_schema: str,
    table_definition: dict,
    source_data_df: pd.DataFrame,
) -> pd.DataFrame:
    log.log(config.VERBOSE, f"starting to add unique id")
    db_conn = db_conn_string
    db_schema = db_schema
    destination_table_name = table_definition["destination_table_name"]
    unique_column_name = "id"

    log.log(config.VERBOSE, destination_table_name)

    query = (
        f"select max({unique_column_name}) from {db_schema}.{destination_table_name};"
    )
    try:
        df = pd.read_sql_query(query, db_conn)
        max_id = df.iloc[0]["max"]
    except Exception:
        max_id = 0
    next_id = int(max_id) + 1

    source_data_df.insert(
        0, unique_column_name, range(next_id, next_id + len(source_data_df))
    )

    return source_data_df


def get_simple_mapping(mapping_definitions: dict) -> dict:
    return {
        k: v for k, v in mapping_definitions.items() if v["casrec_column_name"] != ""
    }


def get_transformations(mapping_definitions: dict) -> dict:
    requires_transformation = {
        k: v
        for k, v in mapping_definitions.items()
        if v["requires_transformation"] != ""
        and v["requires_transformation"] != "date_format_standard"
    }

    transformations = {}
    for k, v in requires_transformation.items():
        tr = v["requires_transformation"]
        d = {"original_columns": v["casrec_column_name"], "aggregate_col": k}
        if tr in transformations:
            transformations[tr].append(d)
        else:
            transformations[tr] = [d]

    return transformations


def get_default_values(mapping_definitions: dict) -> dict:
    return {
        k: v
        for k, v in mapping_definitions.items()
        if v["default_value"] != "" and v["casrec_column_name"] == ""
    }


def get_calculations(mapping_definitions: dict) -> dict:
    requires_calculation = {
        k: v for k, v in mapping_definitions.items() if v["calculated"] != ""
    }

    calculations = {}
    for k, v in requires_calculation.items():
        tr = v["calculated"]
        d = {"column_name": k}
        if tr in calculations:
            calculations[tr].append(d)
        else:
            calculations[tr] = [d]

    return calculations


def get_lookup_tables(mapping_definitions: dict) -> dict:
    return {k: v for k, v in mapping_definitions.items() if v["lookup_table"] != ""}


def perform_transformations(
    mapping_definitions: dict,
    table_definition: dict,
    source_data_df: pd.DataFrame,
    db_conn_string: str,
    db_schema: str,
) -> pd.DataFrame:
    final_df = source_data_df

    log.log(
        config.DATA,
        f"Data before transformations\n{final_df.sample(n=config.row_limit).to_markdown()}",
    )

    simple_mapping = get_simple_mapping(mapping_definitions)
    transformations = get_transformations(mapping_definitions)
    required_columns = get_default_values(mapping_definitions)
    calculated_fields = get_calculations(mapping_definitions)
    lookup_tables = get_lookup_tables(mapping_definitions)

    if len(simple_mapping) > 0:
        final_df = do_simple_mapping(simple_mapping, table_definition, final_df)

    if len(transformations) > 0:
        final_df = do_simple_transformations(transformations, final_df)

    if len(required_columns) > 0:
        final_df = add_required_columns(required_columns, final_df)

    if len(calculated_fields) > 0:
        final_df = do_calculations(calculated_fields, final_df)

    if len(lookup_tables) > 0:
        final_df = map_lookup_tables(lookup_tables, final_df)

    if "id" not in source_data_df.columns.values.tolist():
        final_df = add_unique_id(db_conn_string, db_schema, table_definition, final_df)

    log.log(
        config.DATA,
        f"Data after transformations\n{final_df.sample(n=config.row_limit).to_markdown()}",
    )

    return final_df
