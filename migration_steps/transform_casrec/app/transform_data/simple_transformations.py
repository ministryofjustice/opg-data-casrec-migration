import logging
import os

import pandas as pd
import helpers

from transform_data.conditional_lookups import conditional_lookup
from utilities import standard_transformations

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


def do_simple_transformations(
    transformations: dict, source_data_df: pd.DataFrame
) -> pd.DataFrame:
    log.log(config.VERBOSE, "starting to apply transformations")
    transformed_df = source_data_df

    if "squash_columns" in transformations:
        for t in transformations["squash_columns"]:
            transformed_df = standard_transformations.squash_columns(
                t["original_columns"], t["aggregate_col"], transformed_df
            )
    if "convert_to_bool" in transformations:
        for t in transformations["convert_to_bool"]:
            transformed_df = standard_transformations.convert_to_bool(
                t["original_columns"], t["aggregate_col"], transformed_df
            )
    if "date_format_standard" in transformations:
        for t in transformations["date_format_standard"]:
            transformed_df = standard_transformations.date_format_standard(
                t["original_columns"], t["aggregate_col"], transformed_df
            )
    if "unique_number" in transformations:
        for t in transformations["unique_number"]:
            transformed_df = standard_transformations.unique_number(
                t["aggregate_col"], transformed_df
            )

    if "capitalise" in transformations:
        for t in transformations["capitalise"]:
            transformed_df = standard_transformations.capitalise(
                t["original_columns"], t["aggregate_col"], transformed_df
            )

    if "conditional_lookup" in transformations:
        for t in transformations["conditional_lookup"]:
            transformed_df = conditional_lookup(
                final_col=t["aggregate_col"],
                data_col=t["original_columns"],
                lookup_col=t["lookup_table"][1],
                lookup_file_name=t["lookup_table"][0],
                df=transformed_df,
            )

    return transformed_df
