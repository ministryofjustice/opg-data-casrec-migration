import logging
import os

import pandas as pd
import helpers

from transform_data.conditional_lookups import conditional_lookup
from utilities import standard_transformations

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)
import json


def do_simple_transformations(
    transformations: dict, source_data_df: pd.DataFrame
) -> pd.DataFrame:
    transformed_df = source_data_df

    if "squash_columns" in transformations:
        log.log(config.VERBOSE, "Applying transformation: squash_columns")
        for t in transformations["squash_columns"]:
            transformed_df = standard_transformations.squash_columns(
                t["original_columns"], t["aggregate_col"], transformed_df
            )
    if "convert_to_bool" in transformations:
        log.log(config.VERBOSE, "Applying transformation: convert_to_bool")
        for t in transformations["convert_to_bool"]:
            transformed_df = standard_transformations.convert_to_bool(
                t["original_columns"], t["aggregate_col"], transformed_df
            )
    if "date_format_standard" in transformations:
        log.log(config.VERBOSE, "Applying transformation: date_format_standard")
        for t in transformations["date_format_standard"]:
            transformed_df = standard_transformations.date_format_standard(
                t["original_columns"], t["aggregate_col"], transformed_df
            )
    if "unique_number" in transformations:
        log.log(config.VERBOSE, "Applying transformation: unique_number")
        for t in transformations["unique_number"]:
            transformed_df = standard_transformations.unique_number(
                t["aggregate_col"], transformed_df
            )

    if "capitalise" in transformations:
        log.log(config.VERBOSE, "Applying transformation: capitalise")
        for t in transformations["capitalise"]:
            transformed_df = standard_transformations.capitalise(
                t["original_columns"], t["aggregate_col"], transformed_df
            )

    if "conditional_lookup" in transformations:
        log.log(config.VERBOSE, "Applying transformation: conditional_lookup")
        for t in transformations["conditional_lookup"]:
            transformed_df = conditional_lookup(
                final_col=t["aggregate_col"],
                data_col=t["original_columns"],
                lookup_col=t["additional_columns"],
                lookup_file_name=t["lookup_table"],
                df=transformed_df,
            )

    if "money_poundPence" in transformations:
        log.log(config.VERBOSE, "Applying transformation: money_poundPence")
        for t in transformations["money_poundPence"]:
            transformed_df = standard_transformations.round_column(
                t["original_columns"], t["aggregate_col"], transformed_df
            )

    return transformed_df
