import datetime
import logging
import os
import datetime as dt

import numpy as np

import helpers
import pandas as pd


log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


def format_additional_col_alias(original_column_name: str) -> str:
    return f"c_{original_column_name.lower().replace(' ', '_').replace('.','')}"


def source_conditions(df, conditions):

    convert_to_timestamp_cols = {
        k: v for k, v in conditions.items() if k == "convert_to_timestamp"
    }

    if convert_to_timestamp_cols:
        df = convert_to_timestamp(df, convert_to_timestamp_cols)
        for col in convert_to_timestamp_cols:
            conditions.pop(col, None)

    greater_than_cols = {k: v for k, v in conditions.items() if k == "greater_than"}
    if greater_than_cols:
        df = greater_than(df, greater_than_cols)
        for col in greater_than_cols:
            conditions.pop(col, None)

    less_than_cols = {k: v for k, v in conditions.items() if k == "less_than"}
    if less_than_cols:
        df = less_than(df, less_than_cols)
        for col in less_than_cols:
            conditions.pop(col, None)

    recent_or_open_invoices_cols = {
        k: v for k, v in conditions.items() if k == "recent_or_open_invoices"
    }
    if recent_or_open_invoices_cols:
        df = recent_or_open_invoices(df, recent_or_open_invoices_cols)
        for col in recent_or_open_invoices_cols:
            conditions.pop(col, None)

    date_since_cols = {k: v for k, v in conditions.items() if k == "date_since"}
    if date_since_cols:
        df = date_since(df, date_since_cols)
        for col in date_since_cols:
            conditions.pop(col, None)

    first_x_chars_cols = {k: v for k, v in conditions.items() if k == "first_x_chars"}
    if first_x_chars_cols:
        df = first_x_chars(df, first_x_chars_cols)
        for col in first_x_chars_cols:
            conditions.pop(col, None)

    exclude_values_cols = {k: v for k, v in conditions.items() if k == "exclude_values"}
    if exclude_values_cols:
        df = exclude_values(df, exclude_values_cols)
        for col in exclude_values_cols:
            conditions.pop(col, None)

    include_values_cols = {k: v for k, v in conditions.items() if k == "include_values"}
    if include_values_cols:
        df = include_values(df, include_values_cols)
        for col in include_values_cols:
            conditions.pop(col, None)

    not_null_cols = [k for k, v in conditions.items() if v == "not null"]
    if not_null_cols:
        df = remove_empty_rows(df, not_null_cols)
        for col in not_null_cols:
            conditions.pop(col, None)

    latest_cols = {k: v for k, v in conditions.items() if k == "latest"}
    if latest_cols:
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

    # todo this actually needs fixing not just escaping!
    try:
        for column, value in renamed_conditions.items():
            df = df.loc[df[column] == str(value)]
    except Exception as e:
        log.error(f"Error renaming columns in source conditions: {e}")

    df = df.reset_index(drop=True)
    log.log(config.VERBOSE, f"Dataframe size after applying conditions: {len(df)}")

    return df


def convert_to_timestamp(df, cols):

    empty_data = ["", "NaT", "nan"]

    source_date = format_additional_col_alias(cols["convert_to_timestamp"]["date"])
    source_time = format_additional_col_alias(cols["convert_to_timestamp"]["time"])

    def timestamp(x):
        date = (
            x[source_date][0:10] if x[source_date] not in empty_data else "1900-01-01"
        )
        time = (
            x[source_time].split(".")[0]
            if x[source_time] not in empty_data
            else "00:00:00"
        )

        return dt.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")

    df["c_timestamp"] = (
        df[[source_date, source_time]]
        .astype(str)
        .apply(lambda x: timestamp(x), axis=1,)
    )

    df = df.astype({"c_timestamp": "datetime64[ns]"})

    log.log(
        config.VERBOSE,
        f"Dataframe size after converting {source_date} and {source_time} to timestamp: {len(df)}",
    )

    return df


def exclude_values(df, cols):

    col = format_additional_col_alias(cols["exclude_values"]["col"])
    values_to_exclude = cols["exclude_values"]["values"]

    log.debug(f"Removing rows where '{col}' is one of {values_to_exclude}")

    df = df[~df[col].isin(values_to_exclude)]

    return df

def include_values(df, cols):
    col = format_additional_col_alias(cols["include_values"]["col"])

    values_to_include = cols["include_values"]["values"]

    log.debug(f"Keeping rows where '{col}' is one of {values_to_include}")

    return df[df[col].isin(values_to_include)]

def greater_than(df, cols):
    col = format_additional_col_alias(cols["greater_than"]["col"])
    value = cols["greater_than"]["value"]

    log.debug(f"Removing rows where '{col}' is not greater than {value}")

    df[col] = df[col].astype(float)
    df = df[df[col] > value]

    return df


def less_than(df, cols):
    col = format_additional_col_alias(cols["less_than"]["col"])
    value = cols["less_than"]["value"]

    log.debug(f"Removing rows where '{col}' is not less than {value}")

    df[col] = df[col].astype(float)
    df = df[df[col] < value]

    return df


def recent_or_open_invoices(df, cols):
    # join sop_aged_debt on feeexport to get Open/Closed invoice status
    debt_col = "Outstanding Amount"
    aged_debt_query = f'select "Trx Number", "{debt_col}" from {config.schemas["pre_transform"]}.sop_aged_debt;'
    aged_debt_df = pd.read_sql_query(
        aged_debt_query, config.get_db_connection_string("migration")
    )
    aged_debt_df = aged_debt_df[["Trx Number", debt_col]]

    df = df.merge(
        aged_debt_df, how="left", left_on="Invoice No", right_on="Trx Number",
    )

    filtered_df = filter_recent_or_open_invoices(df=df, cols=cols, debt_col=debt_col)
    filtered_df = filtered_df.drop(columns=["Trx Number", debt_col])

    return filtered_df


def date_since(df, cols):
    col = format_additional_col_alias(cols["date_since"]["col"])
    since_datetime = datetime.datetime.strptime(cols["date_since"]["date"], "%d/%m/%Y")

    log.debug(
        f"Removing rows where '{col}' is before {since_datetime}"
    )

    filtered_df = df[df.apply(lambda x: pd.to_datetime(x[col], dayfirst=True).to_pydatetime() >= since_datetime, axis=1)]

    return filtered_df


def filter_recent_or_open_invoices(df, cols, debt_col):
    col = format_additional_col_alias(cols["recent_or_open_invoices"]["date_col"])
    tax_year_from = cols["recent_or_open_invoices"]["tax_year_from"]
    date_from = datetime.datetime(
        year=tax_year_from, month=3, day=31, hour=23, minute=59, second=59
    )

    log.debug(
        f"Removing rows where '{col}' is on or before {date_from} and {debt_col} is null"
    )

    def is_recent_or_open(date_col, debt_col):
        src_date = pd.to_datetime(date_col, dayfirst=True)
        src_datetime = src_date.to_pydatetime()
        is_recent = src_datetime > date_from
        return is_recent | pd.notnull(debt_col)

    df = df[df.apply(lambda x: is_recent_or_open(x[col], x[debt_col]), axis=1)]

    return df


def first_x_chars(df, cols):

    source_col = format_additional_col_alias(cols["first_x_chars"]["col"])
    result_col = format_additional_col_alias(cols["first_x_chars"]["result_col"])
    num = cols["first_x_chars"]["num"]
    df[result_col] = df[source_col].apply(lambda x: x[:num])

    return df


def select_latest(df, latest_cols):

    col = format_additional_col_alias(latest_cols["latest"]["col"])
    per = format_additional_col_alias(latest_cols["latest"]["per"])

    log.debug(f"Selecting latest '{col}' per '{per}'")

    final_df = df.sort_values(col).groupby(per).tail(1)
    log.log(
        config.VERBOSE,
        f"Dataframe size after selecting latest {col} per {per}: {len(final_df)}",
    )

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

    log.log(
        config.VERBOSE, f"Dataframe size after removing empty rows: {len(final_df)}"
    )

    return final_df
