import logging
import os

import pandas as pd
import helpers

from transform_data.lookup_tables import map_lookup_tables
from utilities.generate_source_query import additional_cols, format_additional_col_alias

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


def conditional_lookup(
    final_col: str,
    lookup_col: str,
    data_col: str,
    lookup_file_name: str,
    df: pd.DataFrame,
) -> pd.DataFrame:

    log.info(f"Doing conditional lookup on {lookup_col} in file {lookup_file_name}")
    log.log(
        config.VERBOSE,
        f"before\n{df.sample(n=config.row_limit).to_markdown()}",
    )

    temp_col = "mapping_col"
    lookup_col = format_additional_col_alias(lookup_col)

    lookup_dict = helpers.get_lookup_dict(lookup_file_name)

    df[temp_col] = df[lookup_col].map(lookup_dict)
    df[temp_col] = df[temp_col].fillna("")

    df[final_col] = df.apply(
        lambda x: x[data_col] if x[temp_col] == data_col else None, axis=1
    )

    log.log(
        config.VERBOSE,
        f"2\n{df.sample(n=config.row_limit).to_markdown()}",
    )

    df = df.drop(columns=[temp_col, data_col])

    log.log(
        config.VERBOSE,
        f"after\n{df.sample(n=config.row_limit).to_markdown()}",
    )

    return df
