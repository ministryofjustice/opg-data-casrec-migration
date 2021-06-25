import sys
import os
from pathlib import Path
from typing import Dict

from pandas.io.json import json_normalize

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import json
import logging
import random
import helpers
import pandas as pd

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


def squash_columns(
    cols_to_squash: list,
    new_col: str,
    df: pd.DataFrame,
    drop_original_cols: bool = True,
    include_keys: bool = False,
) -> pd.DataFrame:

    if include_keys:
        details_dict = df[[x for x in cols_to_squash]].to_dict("records")
        df[new_col] = details_dict

    else:
        df[new_col] = df[cols_to_squash].values.tolist()

    df[new_col] = df[new_col].apply(
        lambda x: json.dumps([x]) if isinstance(x, Dict) else json.dumps(x)
    )

    if drop_original_cols:
        df = df.drop(columns=cols_to_squash)

    return df


def convert_to_bool(
    original_col: str,
    new_col: str,
    df: pd.DataFrame,
    drop_original_col: bool = True,
) -> pd.DataFrame:

    df[new_col] = df[original_col] == "1.0"
    if drop_original_col:
        df = df.drop(columns=original_col)
    return df


def unique_number(new_col: str, df: pd.DataFrame, length: int = 12) -> pd.DataFrame:
    df[new_col] = df.apply(
        lambda x: random.randint(10 ** (length - 1), 10 ** length - 1), axis=1
    )

    return df


def date_format_standard(
    original_col: str, aggregate_col: str, df: pd.DataFrame
) -> pd.DataFrame:
    df["new"] = df[original_col].astype(str)
    df["new"] = pd.to_datetime(df["new"], format="%Y-%m-%d %H:%M:%S")
    df["new"] = [x.strftime("%Y-%m-%d") for x in df.new]

    df = df.drop(columns=original_col)
    df = df.rename(columns={"new": aggregate_col})

    return df


def capitalise(original_col: str, result_col: str, df: pd.DataFrame) -> pd.DataFrame:
    df[result_col] = df[original_col].apply(lambda x: x.upper())
    df = df.drop(columns=[original_col])

    return df


def round_column(
    original_col: str, result_col: str, df: pd.DataFrame, dp=2
) -> pd.DataFrame:

    df = df.replace({original_col: ["", " "]}, "0")
    df[result_col] = df[original_col].apply(lambda x: round(float(x), dp))

    df = df.drop(columns=[original_col])

    return df
