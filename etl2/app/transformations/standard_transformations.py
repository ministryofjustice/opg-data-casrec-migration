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


def convert_to_bool(original_col, new_col, df, drop_original_col=True):
    df[new_col] = df[original_col] == "1.0"
    if drop_original_col:
        df = df.drop(columns=original_col)
    return df


def unique_number(new_col, df, length=12):
    df[new_col] = df.apply(
        lambda x: random.randint(10 ** (length - 1), 10 ** length - 1), axis=1
    )

    return df


def date_format_standard(original_col, aggregate_col, df):
    df["new"] = df[original_col].astype(str)
    df["new"] = pd.to_datetime(df["new"], format="%Y-%m-%d %H:%M:%S")
    df["new"] = [x.strftime("%Y-%m-%d") for x in df.new]

    df = df.drop(columns=original_col)
    df = df.rename(columns={"new": aggregate_col})

    return df


def populate_required_columns(df, required_cols):
    for col, details in required_cols.items():
        df[col] = details["default_value"]

    return df


def get_next_id(db_conn, db_schema, sirius_table_name):
    query = f"select max(id) from {db_schema}.{sirius_table_name};"
    try:
        df = pd.read_sql_query(query, db_conn)
        max_id = df.iloc[0]["max"]
    except Exception:
        max_id = 0
    next_id = int(max_id) + 1

    return next_id


def add_incremental_ids(df, column_name, starting_number):
    df.insert(0, column_name, range(starting_number, starting_number + len(df)))

    return df
