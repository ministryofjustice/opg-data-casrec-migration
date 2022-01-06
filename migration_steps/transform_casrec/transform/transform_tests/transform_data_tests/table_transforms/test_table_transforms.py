import pandas as pd
import pytest

from pandas.testing import assert_frame_equal
from pytest_cases import parametrize_with_cases

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


def case_process_table_transformations_match_once_true():
    # only apply the first mapping which matches:
    # first mapping should be applied to rows 1 and 3;
    # second mapping should be applied to row 2
    return (
        True,
        {
            "c_rev_stat": ["A", "B", "C"],
            "c_review_date": ["2022-01-05", None, "2022-01-06"],
            "status": ["COMPLETE", "DEFAULT_STATUS", "COMPLETE"],
            "reviewstatus": ["REVIEWED", "DEFAULT_REVIEWSTATUS", "REVIEWED"],
        },
    )


def case_process_table_transformations_match_once_false():
    # last mapping should be applied to all rows, even though
    # the first mapping also applies to rows 1 and 3
    return (
        False,
        {
            "c_rev_stat": ["A", "B", "C"],
            "c_review_date": ["2022-01-05", None, "2022-01-06"],
            "status": ["DEFAULT_STATUS", "DEFAULT_STATUS", "DEFAULT_STATUS"],
            "reviewstatus": [
                "DEFAULT_REVIEWSTATUS",
                "DEFAULT_REVIEWSTATUS",
                "DEFAULT_REVIEWSTATUS",
            ],
        },
    )


@parametrize_with_cases(
    "match_once, expected_data",
    cases=".",
    prefix="case_process_table_transformations_match_once",
)
def test_process_table_transformations_match_once(match_once, expected_data):
    """
    If multiple mappings apply to a row but match_once=True, only the first
    matching mapping is applied. If match_once=False, the last of the multiple matching
    mappings is applied.
    """
    df = pd.DataFrame(
        {
            "c_rev_stat": ["A", "B", "C"],
            "c_review_date": ["2022-01-05", None, "2022-01-06"],
        }
    )

    transforms = {
        "t3": {
            "source_cols": ["rev_stat", "review_date"],
            "target_cols": ["status", "reviewstatus"],
        }
    }

    transform_definitions = {
        "t3": {
            "mappings": [
                {
                    "criteria": [
                        'c_rev_stat.isin(["A", "B", "C"])',
                        {"any_set": ["c_review_date"]},
                    ],
                    "output_cols": {"status": "COMPLETE", "reviewstatus": "REVIEWED"},
                },
                {
                    "criteria": ['c_rev_stat.isin(["A", "B", "C"])'],
                    "output_cols": {
                        "status": "DEFAULT_STATUS",
                        "reviewstatus": "DEFAULT_REVIEWSTATUS",
                    },
                },
            ],
            "match_once": match_once,
        }
    }

    actual_df = process_table_transformations(df, transforms, transform_definitions)

    expected_df = pd.DataFrame(expected_data)

    assert_frame_equal(expected_df, actual_df)
