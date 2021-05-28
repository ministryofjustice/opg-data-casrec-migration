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

    for col, details in required_columns.items():
        source_data_df[col] = details["default_value"]

    log.log(
        config.VERBOSE, f"Dataframe size after default columns: {len(source_data_df)}"
    )

    return source_data_df
