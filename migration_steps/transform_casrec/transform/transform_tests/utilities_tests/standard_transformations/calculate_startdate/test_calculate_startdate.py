import pandas as pd

from datetime import datetime
from pytest_cases import parametrize_with_cases

from utilities.standard_transformations import calculate_startdate


# startdate cases (1-4 provided in IN-1123)
def case_calculate_startdate_1():
    return "2021-12-08", "2020-12-09"


def case_calculate_startdate_2():
    return "2020-12-08", "2019-12-09"


def case_calculate_startdate_3():
    return "2019-12-08", "2018-12-09"


def case_calculate_startdate_4():
    return "2018-12-08", "2017-12-09"


def case_calculate_startdate_datetime():
    return datetime.strptime("2021-10-20", "%Y-%m-%d"), "2020-10-21"


def case_calculate_startdate_base_not_a_date():
    return None, None


@parametrize_with_cases(
    "enddate, expected_startdate", cases=".", prefix="case_calculate_startdate"
)
def test_calculate_startdate(enddate, expected_startdate):
    if enddate is not None:
        enddate = pd.Timestamp(enddate)

    test_data = {
        "enddate": [enddate, enddate],
        "startdate": [None, None],
    }

    test_df = pd.DataFrame(test_data)

    result = calculate_startdate("enddate", "startdate", test_df)

    for index, row in result.iterrows():
        if expected_startdate is not None:
            expected_startdate = pd.Timestamp(expected_startdate)
        assert (
            row["startdate"] == expected_startdate
        ), f"startdate value was not correct"
