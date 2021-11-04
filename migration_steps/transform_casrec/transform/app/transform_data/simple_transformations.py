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
    if "get_max_col" in transformations:
        log.log(config.VERBOSE, "Applying transformation: get_max_col")
        for t in transformations["get_max_col"]:
            transformed_df = standard_transformations.get_max_col(
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

    if "multiply_by_100" in transformations:
        log.log(config.VERBOSE, "Applying transformation: multiply_by_100")
        for t in transformations["multiply_by_100"]:
            transformed_df = standard_transformations.multiply_by_100(
                t["original_columns"], t["aggregate_col"], transformed_df
            )

    if "absolute_value" in transformations:
        log.log(config.VERBOSE, "Applying transformation: absolute_value")
        for t in transformations["absolute_value"]:
            transformed_df = standard_transformations.absolute_value(
                t["original_columns"], t["aggregate_col"], transformed_df
            )

    if "first_two_chars" in transformations:
        log.log(config.VERBOSE, "Applying transformation: first_two_chars")
        for t in transformations["first_two_chars"]:
            transformed_df = standard_transformations.first_two_chars(
                t["original_columns"], t["aggregate_col"], transformed_df
            )

    if "add_one_year" in transformations:
        log.log(config.VERBOSE, "Applying transformation: add_one_year")
        for t in transformations["add_one_year"]:
            transformed_df = standard_transformations.add_one_year(
                t["original_columns"], t["aggregate_col"], transformed_df
            )

    if "start_of_tax_year" in transformations:
        log.log(config.VERBOSE, "Applying transformation: start_of_tax_year")
        for t in transformations["start_of_tax_year"]:
            transformed_df = standard_transformations.start_of_tax_year(
                t["original_columns"], t["aggregate_col"], transformed_df
            )

    if "end_of_tax_year" in transformations:
        log.log(config.VERBOSE, "Applying transformation: end_of_tax_year")
        for t in transformations["end_of_tax_year"]:
            transformed_df = standard_transformations.end_of_tax_year(
                t["original_columns"], t["aggregate_col"], transformed_df
            )

    if "fee_reduction_end_date" in transformations:
        log.log(config.VERBOSE, "Applying transformation: fee_reduction_end_date")
        for t in transformations["fee_reduction_end_date"]:
            transformed_df = standard_transformations.fee_reduction_end_date(
                t["original_columns"], t["aggregate_col"], transformed_df
            )

    if "credit_type_from_invoice_ref" in transformations:
        log.log(config.VERBOSE, "Applying transformation: credit_type_from_invoice_ref")
        for t in transformations["credit_type_from_invoice_ref"]:
            transformed_df = standard_transformations.credit_type_from_invoice_ref(
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

    if "calculate_duedate" in transformations:
        log.log(config.VERBOSE, "Applying transformation: calculate_duedate")
        for t in transformations["calculate_duedate"]:
            transformed_df = standard_transformations.calculate_duedate(
                t["original_columns"], t["aggregate_col"], transformed_df
            )

    if "calculate_startdate" in transformations:
        log.log(config.VERBOSE, "Applying transformation: calculate_startdate")
        for t in transformations["calculate_startdate"]:
            transformed_df = standard_transformations.calculate_startdate(
                t["original_columns"], t["aggregate_col"], transformed_df
            )

    if "is_at_least_one_set" in transformations:
        log.log(config.VERBOSE, "Applying transformation: is_at_least_one_set")
        for t in transformations["is_at_least_one_set"]:
            transformed_df = standard_transformations.is_at_least_one_set(
                t["original_columns"], t["aggregate_col"], transformed_df
            )

    log.log(
        config.VERBOSE, f"Dataframe size after transformations: {len(transformed_df)}"
    )

    return transformed_df
