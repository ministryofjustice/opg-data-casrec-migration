import numpy as np
import pandas as pd
import pytest

from pandas.testing import assert_frame_equal
from transform_data.table_transforms import (
    process_table_transformations,
    TableTransformException,
)


def test_process_table_transformations_bad_transform_name():
    df = pd.DataFrame()
    transforms = {"foo": {}}
    transform_definitions = {"bar": {}}

    with pytest.raises(
        TableTransformException, match=r"No table transform named foo exists"
    ):
        process_table_transformations(df, transforms, transform_definitions)


def test_process_table_transformations_df_missing_columns():
    df = pd.DataFrame()

    transforms = {
        "t1": {
            "source_cols": ["Account Number", "Given Name"],
            "target_cols": ["Status", "Review Date"],
        }
    }

    transform_definitions = {"t1": {}}

    expected_message = (
        r"Dataframe is missing source columns required by t1 "
        + "table transform: \\['c_account_number', 'c_given_name'\\]"
    )

    with pytest.raises(TableTransformException, match=expected_message):
        process_table_transformations(df, transforms, transform_definitions)


def test_process_table_transformations_invalid_output_columns():
    df = pd.DataFrame({"c_account_number": [None], "c_given_name": [None]})

    transforms = {
        "t2": {
            "source_cols": ["Account Number", "Given Name"],
            "target_cols": ["status", "reviewdate"],
        }
    }

    transform_definitions = {
        "t2": {
            "local_vars": {},
            "mappings": [
                {
                    "criteria": [],
                    "output_cols": {
                        # valid output column
                        "reviewdate": "2021-11-09",
                        # invalid output column
                        "reviewstatus": "ACKNOWLEDGED",
                    },
                }
            ],
        }
    }

    expected_message = (
        r"Mapping for table transform t2 outputs to column\(s\) "
        + "\\['reviewstatus'\\] which are not specified in target_cols list "
        + "\\['reviewdate', 'status'\\]"
    )

    with pytest.raises(TableTransformException, match=expected_message):
        process_table_transformations(df, transforms, transform_definitions)


def test_process_table_transformations_bad_criteria():
    """Criteria in the mapping mentions a non-existent variable"""
    df = pd.DataFrame({"c_account_number": [None], "c_given_name": [None]})

    transforms = {
        "t2": {
            "source_cols": ["Account Number", "Given Name"],
            "target_cols": ["status", "reviewdate"],
        }
    }

    transform_definitions = {
        "t2": {
            "local_vars": {},
            "mappings": [
                {
                    "criteria": [
                        # here's the error - @account_number_of_interest is not in local_vars
                        "c_account_number == @account_number_of_interest"
                    ],
                    "output_cols": {"reviewdate": "2021-11-09"},
                }
            ],
        }
    }

    with pytest.raises(pd.core.computation.ops.UndefinedVariableError):
        process_table_transformations(df, transforms, transform_definitions)


def test_process_table_transformations_default_cols():
    """
    Default cols can be set using a specific value or a function which
    returns a column derived from the source dataframe.
    """
    source_df = pd.DataFrame(
        {
            "c_lodge_date": ["foo", "bar", "baz", "qux", "quuz", "nix", None, None],
            "c_rcvd_date": ["aaa", None, "", pd.NaT, np.NaN, "bbb", "zuuz", np.NaN],
            "siriuscol": [None, 2, None, 3, "", 4, None, None],
        }
    )

    transforms = {
        "t3": {
            "source_cols": ["Lodge Date"],
            "target_cols": ["c_rcvd_date", "siriuscol"],
        }
    }

    def _set_default_rcvd_date(df):
        df.loc[
            (df["c_lodge_date"] != "")
            & df["c_lodge_date"].notna()
            & (df["c_rcvd_date"].isna() | (df["c_rcvd_date"] == "")),
            "c_rcvd_date",
        ] = df["c_lodge_date"]

        return df["c_rcvd_date"]

    transform_definitions = {
        "t3": {
            "local_vars": {},
            "mappings": [
                {
                    "default_cols": {
                        "c_rcvd_date": _set_default_rcvd_date,
                        "siriuscol": 1,
                    }
                }
            ],
        }
    }

    actual_df = process_table_transformations(
        source_df, transforms, transform_definitions
    )

    expected_df = pd.DataFrame(
        {
            "c_lodge_date": ["foo", "bar", "baz", "qux", "quuz", "nix", None, None],
            "c_rcvd_date": ["aaa", "bar", "baz", "qux", "quuz", "bbb", "zuuz", np.NaN],
            "siriuscol": [1, 1, 1, 1, 1, 1, 1, 1],
        }
    )

    assert_frame_equal(expected_df, actual_df)
