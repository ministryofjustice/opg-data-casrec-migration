import logging
import os

import helpers
import pandas as pd

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


def map_lookup_tables(
    lookup_tables: dict, source_data_df: pd.DataFrame
) -> pd.DataFrame:

    for col, details in lookup_tables.items():
        lookup_table_name = (
            details["lookup_table"][0]
            if len(details["lookup_table"]) == 1
            else details["lookup_table"][1]
        )
        lookup_dict = helpers.get_lookup_dict(file_name=lookup_table_name)

        source_data_df[col] = source_data_df[col].map(lookup_dict)

        source_data_df[col] = source_data_df[col].fillna("")

    return source_data_df
