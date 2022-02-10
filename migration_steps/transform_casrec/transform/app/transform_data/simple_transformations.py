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
    transformed_df = source_data_df

    # These are the transforms we'll try to apply which have identical
    # function signatures
    transforms_to_try = [
        "squash_columns",
        "convert_to_bool",
        "get_max_col",
        "date_format_standard",
        "capitalise",
        "multiply_by_100",
        "absolute_value",
        "first_two_chars",
        "add_one_year",
        "start_of_tax_year",
        "end_of_tax_year",
        "fee_reduction_end_date",
        "credit_type_from_invoice_ref",
        "calculate_duedate",
        "calculate_startdate",
        "is_at_least_one_set",
        "convert_to_timestamp",
        "first_word",
        "last_words",
        "capitalise_first_letter",
        "coalesce",
    ]

    for transform_name in transforms_to_try:
        if transform_name in transformations:
            log.log(config.VERBOSE, f"Applying transformation: {transform_name}")
            for t in transformations[transform_name]:
                transformed_df = getattr(standard_transformations, transform_name)(
                    t["original_columns"], t["aggregate_col"], transformed_df
                )

    # Apply transforms with non-standard signatures or which inexplicably have a different
    # name from the one used in the spreadsheets...
    if "money_poundPence" in transformations:
        log.log(
            config.VERBOSE,
            f"Applying transformation: money_poundPence aka money_to_decimal",
        )
        for t in transformations["money_poundPence"]:
            transformed_df = standard_transformations.money_to_decimal(
                t["original_columns"], t["aggregate_col"], transformed_df
            )

    if "unique_number" in transformations:
        log.log(config.VERBOSE, "Applying transformation: unique_number")
        for t in transformations["unique_number"]:
            transformed_df = standard_transformations.unique_number(
                t["aggregate_col"], transformed_df
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

    log.log(
        config.VERBOSE, f"Dataframe size after transformations: {len(transformed_df)}"
    )

    return transformed_df
