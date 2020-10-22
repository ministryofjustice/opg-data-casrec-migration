import json
import random
import pandas as pd


def squash_columns(
    cols_to_squash: list,
    new_col: str,
    df: pd.DataFrame,
    drop_original_cols: bool = True,
) -> pd.DataFrame:

    df[new_col] = df[cols_to_squash].values.tolist()
    df[new_col] = df[new_col].apply(lambda x: json.dumps(x))

    if drop_original_cols:
        df = df.drop(columns=cols_to_squash)

    return df


def convert_to_bool(
    original_col: str, new_col: str, df: pd.DataFrame, drop_original_col: bool = True,
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
