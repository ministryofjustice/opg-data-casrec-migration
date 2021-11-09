import numpy as np
import pandas as pd

from datetime import datetime
from pytest_cases import parametrize_with_cases

from transform_data.table_transforms import process_table_transformations


_now = np.datetime64(datetime.now().strftime('%Y-%m-%d'))

_rcvd_date_cols = [
    'c_rcvd_date',
    'c_rcvd_date1',
    'c_rcvd_date2',
    'c_rcvd_date3',
    'c_rcvd_date4',
    'c_rcvd_date5',
    'c_rcvd_date6'
]

_sent_date_cols = [
    'c_sent1',
    'c_sent2',
    'c_sent3',
    'c_sent4',
    'c_sent5',
    'c_sent6'
]

def _make_test_data():
    data = {}
    for date_col in _rcvd_date_cols + _sent_date_cols:
        data[date_col] = [None]
    data['c_rev_stat'] = [None]
    data['c_lodge_date'] = [None]
    data['c_review_date'] = [None]
    data['c_further_code'] = [None]
    data['c_followup_date'] = [None]
    data['c_revise_date'] = [None]
    return data

def case_table_transforms_annual_report_lodging_details_acknowledged():
    """  """
    data = _make_test_data()
    data['c_rev_stat'] = ['N']
    data['c_rcvd_date'] = [_now]
    data['c_lodge_date'] = [_now]

    return (
        data,
        'ACKNOWLEDGED'
    )

def case_table_transforms_annual_report_lodging_details_incomplete():
    """  """
    data = _make_test_data()
    data['c_rev_stat'] = ['I']
    data['c_rcvd_date'] = [_now]
    data['c_lodge_date'] = [_now]

    return (
        data,
        'INCOMPLETE'
    )

def case_table_transforms_annual_report_lodging_details_referred_for_review_rev_stat_s():
    """  """
    data = _make_test_data()
    data['c_rev_stat'] = ['S']
    data['c_rcvd_date'] = [_now]
    data['c_lodge_date'] = [_now]

    return (
        data,
        'REFERRED_FOR_REVIEW'
    )

def case_table_transforms_annual_report_lodging_details_referred_for_review_rev_stat_r():
    """  """
    data = _make_test_data()
    data['c_rev_stat'] = ['R']
    data['c_rcvd_date'] = [_now]
    data['c_lodge_date'] = [_now]
    data['c_review_date'] = [_now]

    return (
        data,
        'REFERRED_FOR_REVIEW'
    )

def case_table_transforms_annual_report_lodging_details_referred_for_review_rev_stat_g():
    """  """
    data = _make_test_data()
    data['c_rev_stat'] = ['G']
    data['c_rcvd_date'] = [_now]
    data['c_lodge_date'] = [_now]
    data['c_review_date'] = [_now]

    return (
        data,
        'REFERRED_FOR_REVIEW'
    )

def case_table_transforms_annual_report_lodging_details_referred_for_review_rev_stat_m():
    """  """
    data = _make_test_data()
    data['c_rev_stat'] = ['M']
    data['c_rcvd_date'] = [_now]
    data['c_lodge_date'] = [_now]
    data['c_review_date'] = [_now]

    return (
        data,
        'REFERRED_FOR_REVIEW'
    )

def case_table_transforms_annual_report_lodging_details_incomplete_further_code_234_no_rcvd_date():
    """  """
    data = _make_test_data()
    data['c_revise_date'] = [_now]
    data['c_further_code'] = [2]
    data['c_followup_date'] = [_now]

    return (
        data,
        'INCOMPLETE'
    )

def case_table_transforms_annual_report_lodging_details_incomplete_further_code_234_with_rcvd_date():
    """  """
    data = _make_test_data()
    data['c_revise_date'] = [_now]
    data['c_further_code'] = [2]
    data['c_rcvd_date'] = [_now]
    data['c_followup_date'] = [_now]

    return (
        data,
        'INCOMPLETE'
    )

def case_table_transforms_annual_report_lodging_details_referred_for_review_further_code_18_with_sent_date():
    """  """
    data = _make_test_data()
    data['c_revise_date'] = [_now]
    data['c_further_code'] = [1]
    data['c_sent1'] = [_now]

    return (
        data,
        'REFERRED_FOR_REVIEW'
    )

def case_table_transforms_annual_report_lodging_details_referred_for_review_further_code_18_with_sent_date_and_rcvd_date():
    """  """
    data = _make_test_data()
    data['c_revise_date'] = [_now]
    data['c_further_code'] = [1]
    data['c_rcvd_date'] = [_now]
    data['c_sent1'] = [_now]

    return (
        data,
        'REFERRED_FOR_REVIEW'
    )

def case_table_transforms_annual_report_lodging_details_referred_for_review_all_nulls():
    """  """
    data = _make_test_data()

    return (
        data,
        'REFERRED_FOR_REVIEW'
    )

@parametrize_with_cases("test_data, expected_lodgedstatus", cases=".", prefix="case_table_transforms_annual_report_lodging_details")
def test_table_transforms_annual_report_lodging_details(test_data, expected_lodgedstatus):
    test_df = pd.DataFrame(test_data)

    actual_df = process_table_transformations(test_df, {'set_annual_report_lodging_details_status': {}})

    for _, row in actual_df.iterrows():
        assert row['lodgedstatus'] == expected_lodgedstatus
