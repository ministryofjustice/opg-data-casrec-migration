import logging
import os

import pandas as pd

import helpers


from utilities import standard_calculations


log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


def do_calculations(
    calculated_fields: dict, source_data_df: pd.DataFrame
) -> pd.DataFrame:
    calculations_df = source_data_df

    if "current_date" in calculated_fields:
        for t in calculated_fields["current_date"]:
            calculations_df = standard_calculations.current_date(
                t["column_name"], calculations_df
            )

    return calculations_df
