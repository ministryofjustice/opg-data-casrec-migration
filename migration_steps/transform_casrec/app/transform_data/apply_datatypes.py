import logging
import os
from typing import Dict

import helpers
import pandas as pd

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)

datatype_remap = {"date": "datetime64", "datetime": "datetime64", "dict": "str"}


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

    result_df = df
    # result_df = df.astype({k: v for k, v in cols_with_datatype.items()})
    # result_df = result_df.replace({'NaT': None})

    log.log(
        config.DATA,
        f"Data after datatypes\n{result_df.sample(n=config.row_limit).to_markdown()}",
    )

    return result_df
