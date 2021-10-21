import pandas as pd

from datetime import datetime
from pytest_cases import parametrize_with_cases

from utilities.standard_transformations import calculate_reminderdate


# reminderdate cases
def case_calculate_reminderdate_not_weekend():
    return '2021-10-20', '2021-09-29'

def case_calculate_reminderdate_saturday():
    return '2021-10-02', '2021-09-10'

def case_calculate_reminderdate_sunday():
    return '2021-11-21', '2021-10-29'

def case_calculate_reminderdate_datetime():
    return datetime.strptime('2021-10-20', '%Y-%m-%d'), '2021-09-29'

def case_calculate_reminderdate_base_not_a_date():
    return None, None

@parametrize_with_cases("enddate, expected_reminderdate", cases=".", prefix="case_calculate_reminderdate")
def test_calculate_reminderdate(enddate, expected_reminderdate):
    if enddate is not None:
        enddate = pd.Timestamp(enddate)

    test_data = {
        'enddate': [enddate, enddate],
        'reminderdate': [None, None],
    }

    test_df = pd.DataFrame(test_data)

    result = calculate_reminderdate('enddate', 'reminderdate', test_df)

    for index, row in result.iterrows():
            if expected_reminderdate is not None:
                expected_reminderdate = pd.Timestamp(expected_reminderdate)
            assert row['reminderdate'] == expected_reminderdate, f'reminderdate value was not correct'
