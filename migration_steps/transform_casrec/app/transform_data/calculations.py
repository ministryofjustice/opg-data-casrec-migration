import logging
import os

import pandas as pd

import helpers

from transform_data.conditional_lookups import conditional_lookup
from utilities import standard_calculations


log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


def do_calculations(
    calculated_fields: dict, source_data_df: pd.DataFrame
) -> pd.DataFrame:
    log.log(config.VERBOSE, "starting to apply calculations")
    calculations_df = source_data_df

    if "current_date" in calculated_fields:
        for t in calculated_fields["current_date"]:
            calculations_df = standard_calculations.current_date(
                t["column_name"], calculations_df
            )

    if "conditional_lookup" in calculated_fields:
        for t in calculated_fields["conditional_lookup"]:
            calculations_df = conditional_lookup(
                column_name=t["column_name"],
                original_columns=["casrec_column_name"],
                lookup_file_name=t["lookup_table"],
                df=calculations_df,
            )

    return calculations_df
