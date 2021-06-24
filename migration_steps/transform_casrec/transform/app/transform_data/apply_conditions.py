import logging
import os
import datetime as dt

import numpy as np

import helpers
from custom_errors import EmptyDataFrame


log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


# def convert_to_timestamp(source_date, source_time):
#     date = datetime.strptime(source_date, '%Y-%m-%d')
#     print(f"date: {date}")
#     return datetime.combine(date=date, time=source_time)


def format_additional_col_alias(original_column_name: str) -> str:
    return f"c_{original_column_name.lower().replace(' ', '_').replace('.','')}"


def source_conditions(df, conditions):
    empty_date = ["", "NaT", "nan"]

    try:

        source_date = format_additional_col_alias(
            conditions["convert_to_timestamp"]["date"]
        )
        source_time = format_additional_col_alias(
            conditions["convert_to_timestamp"]["time"]
        )

        df["timestamp"] = (
            df[[source_date, source_time]]
            .astype(str)
            .apply(
                lambda x: dt.datetime.strptime(
                    x[source_date] + x[source_time].split(".")[0], "%Y-%m-%d%H:%M:%S"
                )
                if x[source_date] not in empty_date
                else "",
                axis=1,
            )
        )

        df = df.astype({"timestamp": "datetime64[ns]"})

        conditions.pop("convert_to_timestamp", None)
    except KeyError:
        pass

    not_null_cols = [k for k, v in conditions.items() if v == "not null"]
    df = remove_empty_rows(df, not_null_cols)
    for col in not_null_cols:
        conditions.pop(col, None)

    latest_cols = {k: v for k, v in conditions.items() if k == "latest"}
    df = select_latest(df, latest_cols)
    for col in latest_cols:
        conditions.pop(col, None)

    df_cols = {k: v for k, v in conditions.items() if k in df.columns.tolist()}
    additional_cols = {
        format_additional_col_alias(original_column_name=k): v
        for k, v in conditions.items()
        if k not in df.columns.tolist()
    }
    renamed_conditions = {**df_cols, **additional_cols}

    for column, value in renamed_conditions.items():
        df = df.loc[df[column] == value]

    df = df.reset_index(drop=True)
    log.log(config.VERBOSE, f"Dataframe size after applying conditions: {len(df)}")

    return df


def select_latest(df, latest_cols):

    col = latest_cols["latest"]["col"]
    per = format_additional_col_alias(latest_cols["latest"]["per"])

    log.debug(f"Selecting latest '{col}' per '{per}'")

    final_df = df.sort_values(col).groupby(per).tail(1)

    return final_df


def remove_empty_rows(df, not_null_cols, how="all"):

    if len(not_null_cols) == 0:
        log.debug("No null rows to remove")
        return df

    log.debug(
        f"Removing rows where these fields are all null: {', '.join(not_null_cols)}"
    )

    final_df = df

    cols_to_remove = [x for x in df.columns.tolist() if x in not_null_cols]

    try:
        final_df = final_df.replace("", np.nan)
        final_df = final_df.replace(" ", np.nan)
        final_df = final_df.replace("0", np.nan)

        final_df = final_df.dropna(subset=cols_to_remove, how="all")
        final_df = final_df.reset_index(drop=True)
        final_df = final_df.replace(np.nan, "")

    except Exception as e:
        log.debug(f"Problems removing null rows: {e}")

    log.log(config.VERBOSE, f"Dataframe size after removing empty rows: {len(df)}")

    if len(final_df) == 0:
        raise EmptyDataFrame
    else:
        return final_df
