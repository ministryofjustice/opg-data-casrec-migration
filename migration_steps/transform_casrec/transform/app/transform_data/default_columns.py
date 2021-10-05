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

        default_val = (
            "" if details["default_value"] == "none" else details["default_value"]
        )

        try:
            source_data_df[col] = source_data_df[col].apply(
                lambda x: default_val if x == "" else x
            )
        except Exception:
            source_data_df[col] = default_val

    log.log(
        config.VERBOSE, f"Dataframe size after default columns: {len(source_data_df)}"
    )

    return source_data_df
