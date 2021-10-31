import pandas as pd
import pytest
import re

from datetime import datetime
from pandas.testing import assert_frame_equal
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
        'current_date': [
            {'column_name': 'todays_date'},
            {'column_name': 'another_date'}
        ],
        'uuid4': [
            {'column_name': 'unique_identifier'},
            {'column_name': 'another_identifier'}
        ]
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

def test_do_calculations_unrecognised_calculation():
    # test data
    test_calculations = {
        'no-idea-what-to-do-with-this': [{'column_name': 'duedate'}]
    }

    test_data = {
        'enddate': [None],
        'duedate1': [None],
    }

    test_df = pd.DataFrame(test_data)

    # function under test
    new_df = do_calculations(test_calculations, test_df)

    # dataframe values should not be touched as the calculation is not applied
    assert_frame_equal(test_df, new_df)