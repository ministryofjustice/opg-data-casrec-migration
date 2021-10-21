import re

import pandas as pd

from datetime import datetime
from pytest_cases import parametrize_with_cases

from transform_data.calculations import do_calculations


# creates a function which returns True if the value in the specified column is a UUID4;
# applied to a dataframe to select all rows where column is a UUID
def _make_uuid4_check_fn(column):
    uuid4_regex = re.compile(r'^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
    return lambda row: uuid4_regex.match(f'{row[column]}') != None

def test_do_calculations_multiple_applied():
    # test data
    test_calculations = {
        'current_date': ['todays_date', 'another_date'],
        'uuid4': ['unique_identifier', 'another_identifier']
    }

    untouched_field_values = ['one', 'two', 'three']

    test_data = {
        'todays_date': ['', None, '2021-10-20'],
        'another_date': ['', None, '2021-10-21'],
        'unique_identifier': ['', None, '1'],
        'another_identifier': ['', None, '2'],
        'untouched_field': untouched_field_values,
    }

    test_df = pd.DataFrame(test_data)

    # function under test
    now = datetime.now()
    result = do_calculations(test_calculations, test_df, now)

    # *_date columns should be reset to the current date
    now_str = now.strftime("%Y-%m-%d")
    assert len(result.loc[result['todays_date'] == now_str]) == 3
    assert len(result.loc[result['another_date'] == now_str]) == 3

    # should be UUIDs in the *_identifier columns
    assert len(test_df.apply(_make_uuid4_check_fn('unique_identifier'), axis=1)) == 3
    assert len(test_df.apply(_make_uuid4_check_fn('another_identifier'), axis=1)) == 3

    # untouched_field should contain one of each value across the three rows
    for value in untouched_field_values:
        assert len(result.loc[result['untouched_field'] == value]) == 1

# test data for delta_date calculations; the test cases include both datetimes and strings
# in the reportingperiodenddate, as I'm not sure what type they'll be at this point in
# the transform, so do_calculations() should cope with both
def case_reporting_dates_not_weekend():
    end_date = '2021-10-20'
    expected = {
        'reportingperiodenddate': end_date,
        'duedate': '2021-11-10',
        'reportingperiodstartdate': '2020-10-19',
        'reportduereminderdate': '2021-09-29'
    }
    return end_date, expected

def case_reporting_dates_saturday():
    end_date = '2021-10-02'
    expected = {
        'reportingperiodenddate': end_date,
        'duedate': '2021-10-25',
        'reportingperiodstartdate': '2020-10-01',
        'reportduereminderdate': '2021-09-10'
    }
    return end_date, expected

def case_reporting_dates_sunday():
    end_date = '2021-11-21'
    expected = {
        'reportingperiodenddate': end_date,
        'duedate': '2021-12-13',
        'reportingperiodstartdate': '2020-11-20',
        'reportduereminderdate': '2021-10-29'
    }
    return end_date, expected

def case_reporting_dates_datetime():
    end_date = datetime.strptime('2021-10-20', '%Y-%m-%d')
    expected = {
        'reportingperiodenddate': end_date,
        'duedate': '2021-11-10',
        'reportingperiodstartdate': '2020-10-19',
        'reportduereminderdate': '2021-09-29'
    }
    return end_date, expected

def case_reporting_dates_end_date_is_None():
    end_date = None
    expected = {
        'reportingperiodenddate': end_date,
        'duedate': None,
        'reportingperiodstartdate': None,
        'reportduereminderdate': None
    }
    return end_date, expected

@parametrize_with_cases("end_date, expected", cases=".", prefix="case_reporting_dates")
def test_do_calculations_delta_date(end_date, expected):
    # calculations specific to reporting which use reportingperiodenddate
    # as their baseline
    test_calculations = {
        'delta_date:reportingperiodenddate+21|next-working-day': [
            'duedate'
        ],
        'delta_date:reportingperiodenddate-21|previous-working-day': [
            'reportduereminderdate'
        ],
        'delta_date:reportingperiodenddate-366': [
            'reportingperiodstartdate'
        ],
    }

    # test data: only reportingperiodenddate is set from casrec data,
    # other fields are calculated
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    test_data = {
        'reportingperiodenddate': [end_date],
        'duedate': [None],
        'reportingperiodstartdate': [None],
        'reportduereminderdate': [None],
    }

    test_df = pd.DataFrame(test_data)

    # function under test
    result = do_calculations(test_calculations, test_df)

    # assertions
    for index, row in result.iterrows():
        for column in expected:
            expected_value = expected[column]
            if expected_value is not None:
                expected_value = pd.Timestamp(expected_value)
            assert row[column] == expected_value, f'{column} values did not match'

def test_do_calculations_delta_date_incorrect_formats():
    """ Tests for incorrect delta_date formulae """
    pass