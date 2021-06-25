import logging
import os
from typing import Dict

import helpers
import pandas as pd
import json

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)

datatype_remap = {
    "date": "datetime64[ns]",
    "datetime": "datetime64[ns]",
    "dict": "str",
    "Decimal": "float",
    "text": "str",
}


def apply_datatypes(mapping_details: Dict, df: pd.DataFrame) -> pd.DataFrame:

    log.debug(f"mapping_details: \n{json.dumps(mapping_details, indent=4)}")
    cols_with_datatype = {
        k: v["data_type"]
        if v["data_type"] not in datatype_remap
        else datatype_remap[v["data_type"]]
        for k, v in mapping_details.items()
        if k in df.columns
    }

    log.debug(f"cols_with_datatype: \n{json.dumps(cols_with_datatype, indent=4)}")

    try:
        result_df = df.astype({k: v for k, v in cols_with_datatype.items()})
        result_df.info()
        return result_df
    except Exception as e:
        log.error(f"Error applying datatypes: {e}")
        os._exit(1)


def reapply_datatypes_to_fk_cols(columns, df):
    log.debug("Reapplying fk datatypes")
    for col in columns:
        log.debug(f"Changing {col} to int64")
        df[col] = df[col].astype("Int64")

    return df
