import logging
import os

import pandas as pd

import helpers

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


def do_simple_mapping(
    simple_mapping: dict, table_definition: dict, source_data_df: pd.DataFrame
) -> pd.DataFrame:

    log.log(config.VERBOSE, "starting to apply simple mapping")
    log.log(config.VERBOSE, f"simple mapping dict: {simple_mapping}")

    source_table_name = table_definition["source_table_name"]

    simple_column_remap = [
        {v["alias"]: k}
        for k, v in simple_mapping.items()
        if v["requires_transformation"] == ""
        if v["casrec_table"].lower() == source_table_name
    ]
    columns = {k: v for d in simple_column_remap for k, v in d.items()}

    log.log(
        config.DATA,
        f"Data after simple mapping\n{source_data_df.rename(columns=columns).sample(n=config.row_limit).to_markdown()}",
    )
    return source_data_df.rename(columns=columns)
