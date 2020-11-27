import logging
import os

import pandas as pd
import helpers

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


def add_required_columns(
    required_columns: dict, source_data_df: pd.DataFrame
) -> pd.DataFrame:
    log.log(config.VERBOSE, "starting to apply required columns")
    for col, details in required_columns.items():
        source_data_df[col] = details["default_value"]

    return source_data_df
