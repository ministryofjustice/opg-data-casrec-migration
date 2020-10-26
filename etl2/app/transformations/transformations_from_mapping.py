import pandas as pd
from beeprint import pp

from transformations.standard_transformations import (
    unique_number,
    squash_columns,
    convert_to_bool,
    date_format_standard,
)


def do_simple_mapping(
    simple_mapping: dict, table_definition: dict, source_data_df: pd.DataFrame
) -> pd.DataFrame:

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

    return transformed_df


def add_required_columns(
    required_columns: dict, source_data_df: pd.DataFrame
) -> pd.DataFrame:
    for col, details in required_columns.items():
        source_data_df[col] = details["default_value"]

    return source_data_df


def add_unique_id(
    db_conn_string: str,
    db_schema: str,
    table_definition: dict,
    source_data_df: pd.DataFrame,
) -> pd.DataFrame:
    db_conn = db_conn_string
    db_schema = db_schema
    destination_table_name = table_definition["destination_table_name"]
    unique_column_name = "id"

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

    pp(transformations)
    return transformations


def get_default_values(mapping_definitions: dict) -> dict:
    return {
        k: v
        for k, v in mapping_definitions.items()
        if v["default_value"] != "" and v["casrec_column_name"] == ""
    }


def perform_transformations(
    mapping_definitions: dict,
    table_definition: dict,
    source_data_df: pd.DataFrame,
    db_conn_string: str,
    db_schema: str,
) -> pd.DataFrame:
    final_df = source_data_df

    simple_mapping = get_simple_mapping(mapping_definitions)
    transformations = get_transformations(mapping_definitions)
    required_columns = get_default_values(mapping_definitions)

    if len(simple_mapping) > 0:
        final_df = do_simple_mapping(simple_mapping, table_definition, final_df)

        print(final_df.head().to_markdown())

    if len(transformations) > 0:
        final_df = do_simple_transformations(transformations, final_df)

    if len(required_columns) > 0:
        final_df = add_required_columns(required_columns, final_df)

    final_df = add_unique_id(db_conn_string, db_schema, table_definition, final_df)

    return final_df
