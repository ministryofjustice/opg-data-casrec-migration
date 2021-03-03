import logging
import os
from typing import Dict

import helpers
import pandas as pd

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)

datatype_remap = {
    "date": "datetime64",
    "datetime": "datetime64",
    "dict": "str",
    "Decimal": "float",
}


def apply_datatypes(mapping_details: Dict, df: pd.DataFrame) -> pd.DataFrame:

    log.log(config.VERBOSE, "starting to apply column datatypes")
    log.log(config.VERBOSE, f"datatypes mapping dict: {mapping_details}")

    cols_with_datatype = {
        k: v["data_type"]
        if v["data_type"] not in datatype_remap
        else datatype_remap[v["data_type"]]
        for k, v in mapping_details.items()
        if k in df.columns
    }

    log.log(config.VERBOSE, f"cols_with_datatype: {cols_with_datatype}")

    result_df = df.astype({k: v for k, v in cols_with_datatype.items()})

    log.log(
        config.DATA,
        f"Data after datatypes\n{result_df.sample(n=config.row_limit).to_markdown()}",
    )

    return result_df


def reapply_datatypes_to_fk_cols(columns, df):
    for col in columns:
        df[col] = df[col].astype("Int64")

    return df
