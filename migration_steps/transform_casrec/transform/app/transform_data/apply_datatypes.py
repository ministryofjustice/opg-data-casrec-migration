import logging
import os
from typing import Dict

import helpers
import pandas as pd
import numpy as np

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

    cols_with_datatype = {
        k: v["data_type"]
        if v["data_type"] not in datatype_remap
        else datatype_remap[v["data_type"]]
        for k, v in mapping_details.items()
        if k in df.columns
    }

    for col, datatype in cols_with_datatype.items():
        try:
            if datatype == "datetime64[ns]":
                df[col] = pd.to_datetime(df[col], errors="ignore")
            elif datatype == "bool":
                df[col] = np.where(
                    df[col].isnull(),
                    pd.NA,
                    np.where(
                        df[col] == "true",
                        True,
                        np.where(df[col] == "false", False, df[col]),
                    ),
                )
            else:
                df[col] = df[col].astype(datatype)
        except Exception as e:
            log.error(f"Error converting {col} to datatype {datatype}: {e}")
            os._exit(1)

    return df


def reapply_datatypes_to_fk_cols(columns, df):
    log.debug("Reapplying fk datatypes")
    for col in columns:
        try:
            log.debug(f"Changing {col} to int64")
            df[col] = df[col].astype("float")
            df[col] = df[col].astype("Int64")
        except Exception as e:
            log.error(f"Error reapplying datatypes to fks: {e}")
            os._exit(1)
    return df
