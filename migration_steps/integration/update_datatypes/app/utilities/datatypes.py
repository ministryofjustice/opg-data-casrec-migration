import logging
from typing import Dict

import pandas as pd


datatype_remap = {"date": "datetime64", "datetime": "datetime64", "dict": "str"}


def apply_datatypes(mapping_details: Dict, df: pd.DataFrame) -> pd.DataFrame:
    cols_with_datatype = {
        k: v["data_type"]
        if v["data_type"] not in datatype_remap
        else datatype_remap[v["data_type"]]
        for k, v in mapping_details.items()
    }

    result_df = df.astype({k: v for k, v in cols_with_datatype.items()})

    return result_df
