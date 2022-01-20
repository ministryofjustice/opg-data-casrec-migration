import datetime
import sys
import os
from pathlib import Path
from typing import Dict

from moneyed import Money, GBP

from utilities.df_helpers import get_datetime_from_df_row

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


def capitalise(original_col: str, result_col: str, df: pd.DataFrame) -> pd.DataFrame:
    df[result_col] = df[original_col].apply(lambda x: x.upper())
    df = df.drop(columns=[original_col])

    return df


def multiply_by_100(
    original_col: str, result_col: str, df: pd.DataFrame
) -> pd.DataFrame:
    df[result_col] = df[original_col].apply(
        lambda x: Money(x, GBP).get_amount_in_sub_unit()
    )
    df[result_col] = df[result_col].fillna(0)
    df = df.drop(columns=[original_col])

    return df


def absolute_value(
    original_col: str, result_col: str, df: pd.DataFrame
) -> pd.DataFrame:
    df[result_col] = df[original_col].apply(lambda x: abs(Money(x, GBP).amount))
    df = df.drop(columns=[original_col])

    return df


def first_two_chars(
    original_col: str, result_col: str, df: pd.DataFrame
) -> pd.DataFrame:
    df[result_col] = df[original_col].apply(lambda x: x[:2])
    df = df.drop(columns=[original_col])

    return df


def add_one_year(original_col: str, result_col: str, df: pd.DataFrame) -> pd.DataFrame:
    df[result_col] = df[original_col].astype(str)
    df[result_col] = pd.to_datetime(
        df[result_col], dayfirst=True
    ) + pd.offsets.DateOffset(years=1)
    df = df.drop(columns=[original_col])

    return df


def start_of_tax_year(
    original_col: str, result_col: str, df: pd.DataFrame
) -> pd.DataFrame:
    df[result_col] = df[original_col].astype(str)
    df[result_col] = pd.to_datetime(df[result_col], dayfirst=True)
    df[result_col] = (
        df[result_col]
        .dt.to_period("Q-MAR")
        .dt.qyear.apply(lambda x: datetime.datetime(x - 1, 4, 1))
    )
    df = df.drop(columns=[original_col])

    return df


def end_of_tax_year(
    original_col: str, result_col: str, df: pd.DataFrame
) -> pd.DataFrame:
    df[result_col] = df[original_col].astype(str)
    df[result_col] = pd.to_datetime(df[result_col], dayfirst=True)
    df[result_col] = (
        df[result_col]
        .dt.to_period("Q-MAR")
        .dt.qyear.apply(lambda x: datetime.datetime(x, 3, 31))
    )
    df = df.drop(columns=[original_col])

    return df


def fee_reduction_end_date(
    original_col: str, result_col: str, df: pd.DataFrame
) -> pd.DataFrame:
    df[result_col] = df[original_col].astype(str)
    df[result_col] = pd.to_datetime(df[result_col], dayfirst=True)

    def end_date_from_award_date(x: datetime.datetime):
        date = x.strftime("%d/%m")
        if date == "31/03":
            return x
        if date == "01/04":
            return x - datetime.timedelta(days=1)
        # default to end of Award Date's tax year
        tax_year_end = x.replace(day=31, month=3)
        if x > tax_year_end:
            tax_year_end = tax_year_end.replace(
                year=int(tax_year_end.strftime("%Y")) + 1
            )
        return tax_year_end

    df[result_col] = df[result_col].apply(lambda x: end_date_from_award_date(x))
    df = df.drop(columns=[original_col])

    return df


def credit_type_from_invoice_ref(
    original_col: str, result_col: str, df: pd.DataFrame
) -> pd.DataFrame:
    df[result_col] = df[original_col].apply(lambda x: get_credit_type(x))
    df = df.drop(columns=[original_col])
    return df


def get_credit_type(invoice_ref: str) -> str:
    if invoice_ref[:1] == "Z" or invoice_ref[-1:] == "Z":
        return "CREDIT REMISSION"
    elif invoice_ref[:2] == "CR" or invoice_ref[-2:] == "CR":
        return "CREDIT MEMO"
    elif invoice_ref[:2] == "WO" or invoice_ref[-2:] == "WO":
        return "CREDIT WRITE OFF"


def money_to_decimal(
    original_col: str, result_col: str, df: pd.DataFrame
) -> pd.DataFrame:

    df = df.replace({original_col: ["", " "]}, "0")
    df[result_col] = df[original_col].apply(lambda x: Money(x, GBP).amount)

    df = df.drop(columns=[original_col])

    return df


def get_max_col(original_cols: list, result_col: str, df: pd.DataFrame) -> pd.DataFrame:

    try:
        df[original_cols] = df[original_cols].astype("float64")
    except Exception:
        pass

    df["temp"] = df[original_cols].values.tolist()
    df[result_col] = df["temp"].apply(lambda x: max(x))

    df = df.drop(columns=original_cols)
    df = df.drop(columns=["temp"])

    return df


# base_date: date to use as the basis for the delta date in DD/MM/YYYY format
# operator: delta modifier, '+' or '-'
# days: delta number of days
# weekend_adjustment: 'previous' or 'next' or None;
#     if 'previous' and calculated date is on a weekend, move to previous working day;
#     if 'next' and calculated date is on a weekend, move to next working day;
#     if None, apply no adjustment
# return: datetime, or None if the base_date is None or ""
def _calculate_date(base_date, delta: pd.DateOffset, weekend_adjustment: str = None):
    if base_date is None or base_date == "":
        return None

    new_date = pd.to_datetime(base_date, dayfirst=True)
    new_date = new_date + delta

    # Saturday, Sunday = [5, 6]
    weekday = new_date.weekday()
    if weekday in [5, 6]:
        if weekend_adjustment == "previous":
            new_date = new_date - pd.offsets.DateOffset(days=weekday - 4)
        elif weekend_adjustment == "next":
            new_date = new_date + pd.offsets.DateOffset(days=7 - weekday)

    return new_date


def calculate_duedate(
    original_col: str, result_col: str, df: pd.DataFrame
) -> pd.DataFrame:
    df[result_col] = df[original_col].apply(
        lambda base_date: _calculate_date(
            base_date=base_date,
            delta=pd.offsets.DateOffset(days=21),
            weekend_adjustment="next",
        )
    )
    return df


def calculate_startdate(
    original_col: str, result_col: str, df: pd.DataFrame
) -> pd.DataFrame:
    df[result_col] = df[original_col].apply(
        lambda base_date: _calculate_date(
            base_date=base_date, delta=pd.offsets.DateOffset(days=1, years=-1)
        )
    )
    return df


def is_at_least_one_set(
    original_cols: list, result_col: str, df: pd.DataFrame
) -> pd.DataFrame:
    """
    Set result_col to true if at least one of the values in the columns
    original_cols has a non-null/non-NaT/non-NaN etc. value
    """

    def _transform(row):
        result = False

        for column in original_cols:
            value = row[column]
            if value is not None and value != "":
                result = True
                break

        row[result_col] = result
        return row

    return df.apply(_transform, axis=1)


def convert_to_timestamp(
    original_cols: list, result_col: str, df: pd.DataFrame
) -> pd.DataFrame:
    df[result_col] = df[original_cols].apply(
        lambda x: get_datetime_from_df_row(
            row=x, date_col=original_cols[0], time_col=original_cols[1]
        ),
        axis=1,
    )
    df[result_col] = df[result_col].astype("datetime64[ns]")
    df[result_col] = df[result_col].dt.tz_localize("Europe/London").dt.tz_convert("UTC")

    df = df.drop(columns=original_cols)

    return df


def first_word(original_col: str, result_col: str, df: pd.DataFrame) -> pd.DataFrame:
    df[result_col] = df[original_col].apply(
        lambda x: x.split(" ", 1)[0].title(),
    )

    df = df.drop(columns=[original_col])

    return df


def last_words(original_col: str, result_col: str, df: pd.DataFrame) -> pd.DataFrame:
    def f(x):
        parts = x.split(" ", 1)
        return parts[1].title() if len(parts) == 2 else ""

    df[result_col] = df[original_col].apply(f)
    df = df.drop(columns=[original_col])

    return df


def capitalise_first_letter(
    original_col: str, result_col: str, df: pd.DataFrame
) -> pd.DataFrame:
    df[result_col] = df[original_col].apply(lambda x: x.title())

    df = df.drop(columns=[original_col])

    return df
