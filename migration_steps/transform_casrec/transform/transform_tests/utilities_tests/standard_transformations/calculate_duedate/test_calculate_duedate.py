import pandas as pd

from datetime import datetime
from pytest_cases import parametrize_with_cases

from utilities.standard_transformations import calculate_duedate


# duedate cases
def case_calculate_duedate_not_weekend():
    return "2021-10-20", "2021-11-10"


def case_calculate_duedate_saturday():
    return "2021-10-02", "2021-10-25"


def case_calculate_duedate_sunday():
    return "2021-11-21", "2021-12-13"


def case_calculate_duedate_datetime():
    return datetime.strptime("2021-10-20", "%Y-%m-%d"), "2021-11-10"


def case_calculate_duedate_base_not_a_date():
    return None, None


@parametrize_with_cases(
    "enddate, expected_duedate", cases=".", prefix="case_calculate_duedate"
)
def test_calculate_duedate(enddate, expected_duedate):
    if enddate is not None:
        enddate = pd.Timestamp(enddate)

    test_data = {
        "enddate": [enddate, enddate],
        "duedate": [None, None],
    }

    test_df = pd.DataFrame(test_data)

    result = calculate_duedate("enddate", "duedate", test_df)

    for index, row in result.iterrows():
        if expected_duedate is not None:
            expected_duedate = pd.Timestamp(expected_duedate)
        assert row["duedate"] == expected_duedate, f"duedate value was not correct"
