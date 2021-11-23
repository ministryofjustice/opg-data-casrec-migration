import numpy as np
import pandas as pd

from datetime import datetime
from pytest_cases import parametrize_with_cases

from transform_data.table_transforms import process_table_transformations


NOW = np.datetime64(datetime.now().strftime('%Y-%m-%d'))
SEVEN_DAYS_FROM_NOW = np.busday_offset(NOW, 7)
FOURTEEN_WORKING_DAYS_AGO = np.busday_offset(NOW, -14)
THIRTY_WORKING_DAYS_AGO = np.busday_offset(NOW, -30)
SEVENTY_ONE_WORKING_DAYS_AGO = np.busday_offset(NOW, -71)

# date columns we check for null values
_all_date_cols = [
    'c_rcvd_date',
    'c_rcvd_date1',
    'c_rcvd_date2',
    'c_rcvd_date3',
    'c_rcvd_date4',
    'c_rcvd_date5',
    'c_rcvd_date6',
    'c_lodge_date',
    'c_review_date',
    'c_end_date'
]

def _make_test_data():
    data = {}
    for col in _all_date_cols:
        data[col] = [None]
    data['c_rev_stat'] = [None]
    data['c_next_yr'] = [None]
    return data

def case_table_transforms_annual_report_logs_pending_no_review():
    """ rev stat = 'N', end date in future, all other dates null """
    data = _make_test_data()
    data['c_rev_stat'] = ['N']
    data['c_end_date'] = [SEVEN_DAYS_FROM_NOW]

    return (
        data,
        {
            'status': 'PENDING',
            'reviewstatus': 'NO_REVIEW'
        }
    )

def case_table_transforms_annual_report_logs_due_no_review():
    """ rev stat = 'N', end date in past but < 15 working days ago, all other dates null """
    data = _make_test_data()
    data['c_rev_stat'] = ['N']
    data['c_end_date'] = [FOURTEEN_WORKING_DAYS_AGO]

    return (
        data,
        {
            'status': 'DUE',
            'reviewstatus': 'NO_REVIEW'
        }
    )

def case_table_transforms_annual_report_logs_overdue_no_review():
    """
    rev stat = 'N', end date at least 15 days ago but less than 71 days ago,
    all other dates null
    """
    data = _make_test_data()
    data['c_rev_stat'] = ['N']
    data['c_end_date'] = [THIRTY_WORKING_DAYS_AGO]

    return (
        data,
        {
            'status': 'OVERDUE',
            'reviewstatus': 'NO_REVIEW'
        }
    )

def case_table_transforms_annual_report_logs_non_compliant_no_review():
    """
    rev stat = 'N', end date 71+ days ago, all other dates null
    """
    data = _make_test_data()
    data['c_rev_stat'] = ['N']
    data['c_end_date'] = [SEVENTY_ONE_WORKING_DAYS_AGO]

    return (
        data,
        {
            'status': 'NON_COMPLIANT',
            'reviewstatus': 'NO_REVIEW'
        }
    )

def case_table_transforms_annual_report_logs_received_no_review():
    """
    rev stat = 'N', at least one rcvd date col set, lodge date and review date not set
    """
    data = _make_test_data()
    data['c_rev_stat'] = ['N']
    data['c_rcvd_date'] = [SEVENTY_ONE_WORKING_DAYS_AGO]

    return (
        data,
        {
            'status': 'RECEIVED',
            'reviewstatus': 'NO_REVIEW'
        }
    )

def case_table_transforms_annual_report_logs_received_lodged():
    """
    rev stat = 'N', at least one rcvd date col set, lodge date set, review date not set
    """
    data = _make_test_data()
    data['c_rev_stat'] = ['N']
    data['c_rcvd_date'] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data['c_rcvd_date1'] = [THIRTY_WORKING_DAYS_AGO]
    data['c_lodge_date'] = [THIRTY_WORKING_DAYS_AGO]

    return (
        data,
        {
            'status': 'LODGED',
            'reviewstatus': 'NO_REVIEW'
        }
    )

def case_table_transforms_annual_report_logs_incomplete_no_review():
    """
    rev stat = 'I', at least one rcvd date col set, lodge date set, review date not set
    """
    data = _make_test_data()
    data['c_rev_stat'] = ['I']
    data['c_rcvd_date'] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data['c_rcvd_date1'] = [THIRTY_WORKING_DAYS_AGO]
    data['c_rcvd_date2'] = [FOURTEEN_WORKING_DAYS_AGO]
    data['c_lodge_date'] = [FOURTEEN_WORKING_DAYS_AGO]

    return (
        data,
        {
            'status': 'INCOMPLETE',
            'reviewstatus': 'NO_REVIEW'
        }
    )

def case_table_transforms_annual_report_logs_lodged_staff_referred():
    """
    rev stat = 'S', at least one rcvd date col set, lodge date set, review date not set
    """
    data = _make_test_data()
    data['c_rev_stat'] = ['S']
    data['c_rcvd_date'] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data['c_rcvd_date1'] = [THIRTY_WORKING_DAYS_AGO]
    data['c_rcvd_date2'] = [FOURTEEN_WORKING_DAYS_AGO]
    data['c_lodge_date'] = [FOURTEEN_WORKING_DAYS_AGO]

    return (
        data,
        {
            'status': 'LODGED',
            'reviewstatus': 'STAFF_REFERRED'
        }
    )

def case_table_transforms_annual_report_logs_rev_stat_s_lodged_reviewed():
    """
    rev stat = 'S', at least one rcvd date col set, lodge date set, review date set
    """
    data = _make_test_data()
    data['c_rev_stat'] = ['S']
    data['c_rcvd_date'] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data['c_rcvd_date1'] = [THIRTY_WORKING_DAYS_AGO]
    data['c_lodge_date'] = [THIRTY_WORKING_DAYS_AGO]
    data['c_review_date'] = [FOURTEEN_WORKING_DAYS_AGO]

    return (
        data,
        {
            'status': 'LODGED',
            'reviewstatus': 'REVIEWED'
        }
    )

def case_table_transforms_annual_report_logs_rev_stat_r_lodged_reviewed():
    """
    rev stat = 'R', at least one rcvd date col set, lodge date set, review date set
    """
    data = _make_test_data()
    data['c_rev_stat'] = ['R']
    data['c_rcvd_date'] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data['c_rcvd_date1'] = [THIRTY_WORKING_DAYS_AGO]
    data['c_lodge_date'] = [THIRTY_WORKING_DAYS_AGO]
    data['c_review_date'] = [FOURTEEN_WORKING_DAYS_AGO]

    return (
        data,
        {
            'status': 'LODGED',
            'reviewstatus': 'REVIEWED'
        }
    )

def case_table_transforms_annual_report_logs_rev_stat_g_lodged_reviewed():
    """
    rev stat = 'G', at least one rcvd date col set, lodge date set, review date set
    """
    data = _make_test_data()
    data['c_rev_stat'] = ['G']
    data['c_rcvd_date'] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data['c_rcvd_date1'] = [THIRTY_WORKING_DAYS_AGO]
    data['c_lodge_date'] = [THIRTY_WORKING_DAYS_AGO]
    data['c_review_date'] = [FOURTEEN_WORKING_DAYS_AGO]

    return (
        data,
        {
            'status': 'LODGED',
            'reviewstatus': 'REVIEWED'
        }
    )

def case_table_transforms_annual_report_logs_rev_stat_m_lodged_reviewed():
    """
    rev stat = 'M', at least one rcvd date col set, lodge date set, review date set
    """
    data = _make_test_data()
    data['c_rev_stat'] = ['M']
    data['c_rcvd_date'] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data['c_rcvd_date1'] = [THIRTY_WORKING_DAYS_AGO]
    data['c_lodge_date'] = [THIRTY_WORKING_DAYS_AGO]
    data['c_review_date'] = [FOURTEEN_WORKING_DAYS_AGO]

    return (
        data,
        {
            'status': 'LODGED',
            'reviewstatus': 'REVIEWED'
        }
    )

def case_table_transforms_annual_report_logs_abandoned_no_review():
    """
    rev stat = 'X', no date cols set
    """
    data = _make_test_data()
    data['c_rev_stat'] = ['X']

    return (
        data,
        {
            'status': 'ABANDONED',
            'reviewstatus': 'NO_REVIEW'
        }
    )

def case_table_transforms_annual_report_logs_pending_staff_preselected():
    """
    rev stat not set, end date in the future, other date cols not set, `Next Yr` is "Y"
    """
    data = _make_test_data()
    data['c_end_date'] = [SEVEN_DAYS_FROM_NOW]
    data['c_next_yr'] = ['Y']

    return (
        data,
        {
            'status': 'PENDING',
            'reviewstatus': 'STAFF_PRESELECTED'
        }
    )

@parametrize_with_cases("test_data, expected_data", cases=".", prefix="case_table_transforms_annual_report_logs")
def test_table_transforms_annual_report_logs(test_data, expected_data):
    test_df = pd.DataFrame(test_data)

    transforms = {
        'set_annual_report_logs_status': {
            'source_cols': [
                'Rev Stat',
                'End Date',
                'Lodge Date',
                'Rcvd Date',
                'Rcvd Date1',
                'Rcvd Date2',
                'Rcvd Date3',
                'Rcvd Date4',
                'Rcvd Date5',
                'Rcvd Date6',
                'Review Date',
                'Next Yr'
            ],
            'target_cols': [
                'status',
                'reviewstatus'
            ]
        }
    }

    actual_df = process_table_transformations(test_df, transforms)

    for _, row in actual_df.iterrows():
        for col, value in expected_data.items():
            assert row[col] == value
