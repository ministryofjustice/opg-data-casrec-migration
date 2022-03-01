import numpy as np
import pandas as pd

from datetime import datetime
from pytest_cases import parametrize_with_cases

from transform_data.table_transforms import process_table_transformations


NOW = np.datetime64(datetime.now().strftime("%Y-%m-%d"))
SEVEN_DAYS_FROM_NOW = np.busday_offset(NOW, 7, roll="forward")
FOURTEEN_WORKING_DAYS_AGO = np.busday_offset(NOW, -14, roll="forward")
THIRTY_WORKING_DAYS_AGO = np.busday_offset(NOW, -30, roll="forward")
SEVENTY_ONE_WORKING_DAYS_AGO = np.busday_offset(NOW, -71, roll="forward")

# date columns we check for null values
_all_date_cols = [
    "c_rcvd_date",
    "c_rcvd_date1",
    "c_rcvd_date2",
    "c_rcvd_date3",
    "c_rcvd_date4",
    "c_rcvd_date5",
    "c_rcvd_date6",
    "c_lodge_date",
    "c_review_date",
    "c_end_date",
]


def _make_test_data():
    data = {}
    for col in _all_date_cols:
        data[col] = [None]
    data["c_rev_stat"] = [None]
    data["c_next_yr"] = [None]
    return data


def case_table_transforms_annual_report_logs_rev_stat_n_no_dates_future_end_date():
    """rev stat = 'N', end date in future, all other dates null"""
    data = _make_test_data()
    data["c_rev_stat"] = ["N"]
    data["c_end_date"] = [SEVEN_DAYS_FROM_NOW]

    return (data, {"status": "PENDING", "reviewstatus": "NO_REVIEW"})


def case_table_transforms_annual_report_logs_rev_stat_n_no_dates_end_date_passed1():
    """rev stat = 'N', end date in past but < 15 working days ago, all other dates null"""
    data = _make_test_data()
    data["c_rev_stat"] = ["N"]
    data["c_end_date"] = [FOURTEEN_WORKING_DAYS_AGO]

    return (data, {"status": "DUE", "reviewstatus": "NO_REVIEW"})


def case_table_transforms_annual_report_logs_rev_stat_n_no_dates_end_date_passed2():
    """
    rev stat = 'N', end date at least 15 days ago but less than 71 days ago,
    all other dates null
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["N"]
    data["c_end_date"] = [THIRTY_WORKING_DAYS_AGO]

    return (data, {"status": "OVERDUE", "reviewstatus": "NO_REVIEW"})


def case_table_transforms_annual_report_logs_rev_stat_n_no_dates_end_date_passed3():
    """
    rev stat = 'N', end date 71+ days ago, all other dates null
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["N"]
    data["c_end_date"] = [SEVENTY_ONE_WORKING_DAYS_AGO]

    return (data, {"status": "NON_COMPLIANT", "reviewstatus": "NO_REVIEW"})


def case_table_transforms_annual_report_logs_rev_stat_n_no_lodge_or_review_dates():
    """
    rev stat = 'N', at least one rcvd date set, lodge date and review date not set
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["N"]
    data["c_rcvd_date"] = [SEVENTY_ONE_WORKING_DAYS_AGO]

    return (data, {"status": "RECEIVED", "reviewstatus": "NO_REVIEW"})


def case_table_transforms_annual_report_logs_rev_stat_n_no_review_date():
    """
    rev stat = 'N', at least one rcvd date set, lodge date set, review date not set
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["N"]
    data["c_rcvd_date"] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data["c_rcvd_date1"] = [THIRTY_WORKING_DAYS_AGO]
    data["c_lodge_date"] = [THIRTY_WORKING_DAYS_AGO]

    return (data, {"status": "LODGED", "reviewstatus": "NO_REVIEW"})


def case_table_transforms_annual_report_logs_rev_stat_n_all_dates_set():
    """
    rev stat = 'N', at least one rcvd date set, lodge date set, review date set
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["N"]
    data["c_rcvd_date"] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data["c_rcvd_date1"] = [THIRTY_WORKING_DAYS_AGO]
    data["c_lodge_date"] = [THIRTY_WORKING_DAYS_AGO]
    data["c_review_date"] = [THIRTY_WORKING_DAYS_AGO]

    return (data, {"status": "LODGED", "reviewstatus": None})


def case_table_transforms_annual_report_logs_rev_stat_i_no_review_date():
    """
    rev stat = 'I', at least one rcvd date set, lodge date set, review date not set
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["I"]
    data["c_rcvd_date"] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data["c_rcvd_date1"] = [THIRTY_WORKING_DAYS_AGO]
    data["c_rcvd_date2"] = [FOURTEEN_WORKING_DAYS_AGO]
    data["c_lodge_date"] = [FOURTEEN_WORKING_DAYS_AGO]

    return (data, {"status": "INCOMPLETE", "reviewstatus": "NO_REVIEW"})


def case_table_transforms_annual_report_logs_rev_stat_i_all_dates_set():
    """
    rev stat = 'I', at least one rcvd date set, lodge date set, review date set
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["I"]
    data["c_rcvd_date"] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data["c_rcvd_date1"] = [THIRTY_WORKING_DAYS_AGO]
    data["c_rcvd_date2"] = [FOURTEEN_WORKING_DAYS_AGO]
    data["c_lodge_date"] = [FOURTEEN_WORKING_DAYS_AGO]
    data["c_review_date"] = [FOURTEEN_WORKING_DAYS_AGO]

    return (data, {"status": "INCOMPLETE", "reviewstatus": "NO_REVIEW"})


def case_table_transforms_annual_report_logs_rev_stat_s_no_review_date():
    """
    rev stat = 'S', at least one rcvd date set, lodge date set, review date not set
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["S"]
    data["c_rcvd_date"] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data["c_rcvd_date1"] = [THIRTY_WORKING_DAYS_AGO]
    data["c_rcvd_date2"] = [FOURTEEN_WORKING_DAYS_AGO]
    data["c_lodge_date"] = [FOURTEEN_WORKING_DAYS_AGO]

    return (data, {"status": "LODGED", "reviewstatus": "STAFF_REFERRED"})


def case_table_transforms_annual_report_logs_rev_stat_s_all_dates_set():
    """
    rev stat = 'S', at least one rcvd date set, lodge date set, review date set
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["S"]
    data["c_rcvd_date"] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data["c_rcvd_date1"] = [THIRTY_WORKING_DAYS_AGO]
    data["c_lodge_date"] = [THIRTY_WORKING_DAYS_AGO]
    data["c_review_date"] = [FOURTEEN_WORKING_DAYS_AGO]

    return (data, {"status": "LODGED", "reviewstatus": "REVIEWED"})


def case_table_transforms_annual_report_logs_rev_stat_s_no_lodge_or_review_dates():
    """
    rev stat = 'S', at least one rcvd date set, lodge date not set, review date not set
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["S"]
    data["c_rcvd_date"] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data["c_rcvd_date1"] = [THIRTY_WORKING_DAYS_AGO]

    return (data, {"status": "DUE", "reviewstatus": "STAFF_REFERRED"})


def case_table_transforms_annual_report_logs_rev_stat_s_no_dates_set():
    """
    rev stat = 'S', rcvd date not set, lodge date not set, review date not set
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["S"]

    return (data, {"status": "OVERDUE", "reviewstatus": None})


def case_table_transforms_annual_report_logs_rev_stat_r_all_dates_set():
    """
    rev stat = 'R', at least one rcvd date set, lodge date set, review date set
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["R"]
    data["c_rcvd_date"] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data["c_rcvd_date1"] = [THIRTY_WORKING_DAYS_AGO]
    data["c_lodge_date"] = [THIRTY_WORKING_DAYS_AGO]
    data["c_review_date"] = [FOURTEEN_WORKING_DAYS_AGO]

    return (data, {"status": "LODGED", "reviewstatus": "REVIEWED"})


def case_table_transforms_annual_report_logs_rev_stat_r_no_dates_set():
    """
    rev stat = 'R', rcvd date not set, lodge date not set, review date not set
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["R"]

    return (data, {"status": "OVERDUE", "reviewstatus": None})


def case_table_transforms_annual_report_logs_rev_stat_r_no_review_date():
    """
    rev stat = 'R', rcvd date set, lodge date set, review date not set
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["R"]
    data["c_rcvd_date"] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data["c_rcvd_date1"] = [THIRTY_WORKING_DAYS_AGO]
    data["c_lodge_date"] = [THIRTY_WORKING_DAYS_AGO]

    return (data, {"status": "OVERDUE", "reviewstatus": None})


def case_table_transforms_annual_report_logs_rev_stat_r_no_lodge_or_review_dates():
    """
    rev stat = 'R', rcvd date set, lodge date not set, review date not set
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["R"]
    data["c_rcvd_date"] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data["c_rcvd_date1"] = [THIRTY_WORKING_DAYS_AGO]

    return (data, {"status": "DUE", "reviewstatus": "STAFF_REFERRED"})


def case_table_transforms_annual_report_logs_rev_stat_g_all_dates_set():
    """
    rev stat = 'G', at least one rcvd date set, lodge date set, review date set
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["G"]
    data["c_rcvd_date"] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data["c_rcvd_date1"] = [THIRTY_WORKING_DAYS_AGO]
    data["c_lodge_date"] = [THIRTY_WORKING_DAYS_AGO]
    data["c_review_date"] = [FOURTEEN_WORKING_DAYS_AGO]

    return (data, {"status": "LODGED", "reviewstatus": "REVIEWED"})


def case_table_transforms_annual_report_logs_rev_stat_g_no_review_date():
    """
    rev stat = 'G', at least one rcvd date set, lodge date set, review date not set
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["G"]
    data["c_rcvd_date"] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data["c_rcvd_date1"] = [THIRTY_WORKING_DAYS_AGO]
    data["c_lodge_date"] = [THIRTY_WORKING_DAYS_AGO]

    return (data, {"status": "LODGED", "reviewstatus": "STAFF_REFERRED"})


def case_table_transforms_annual_report_logs_rev_stat_m_all_dates_set():
    """
    rev stat = 'M', at least one rcvd date set, lodge date set, review date set
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["M"]
    data["c_rcvd_date"] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data["c_rcvd_date1"] = [THIRTY_WORKING_DAYS_AGO]
    data["c_lodge_date"] = [THIRTY_WORKING_DAYS_AGO]
    data["c_review_date"] = [FOURTEEN_WORKING_DAYS_AGO]

    return (data, {"status": "LODGED", "reviewstatus": "REVIEWED"})


def case_table_transforms_annual_report_logs_rev_stat_x_all_dates_set():
    """
    rev stat = 'X', at least one rcvd date set, lodge date set, review date set
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["X"]
    data["c_rcvd_date"] = [SEVENTY_ONE_WORKING_DAYS_AGO]
    data["c_rcvd_date1"] = [THIRTY_WORKING_DAYS_AGO]
    data["c_lodge_date"] = [THIRTY_WORKING_DAYS_AGO]
    data["c_review_date"] = [FOURTEEN_WORKING_DAYS_AGO]

    return (data, {"status": "ABANDONED", "reviewstatus": "NO_REVIEW"})


def case_table_transforms_annual_report_logs_rev_stat_x_no_dates_set():
    """
    rev stat = 'X', no date cols set
    """
    data = _make_test_data()
    data["c_rev_stat"] = ["X"]

    return (data, {"status": "ABANDONED", "reviewstatus": "NO_REVIEW"})


def case_table_transforms_annual_report_logs_rev_stat_not_set():
    """
    rev stat not set, end date in the future, other date cols not set, `Next Yr` is "Y"
    """
    data = _make_test_data()
    data["c_end_date"] = [SEVEN_DAYS_FROM_NOW]
    data["c_next_yr"] = ["Y"]

    return (data, {"status": "PENDING", "reviewstatus": "STAFF_PRESELECTED"})


@parametrize_with_cases(
    "test_data, expected_data",
    cases=".",
    prefix="case_table_transforms_annual_report_logs",
)
def test_table_transforms_annual_report_logs(test_data, expected_data):
    test_df = pd.DataFrame(test_data)

    transforms = {
        "set_annual_report_logs_status": {
            "source_cols": [
                "Rev Stat",
                "End Date",
                "Lodge Date",
                "Rcvd Date",
                "Rcvd Date1",
                "Rcvd Date2",
                "Rcvd Date3",
                "Rcvd Date4",
                "Rcvd Date5",
                "Rcvd Date6",
                "Review Date",
                "Next Yr",
            ],
            "target_cols": [
                "status",
                "reviewstatus",
                "c_rcvd_date",
            ],
        }
    }

    actual_df = process_table_transformations(test_df, transforms)

    for _, row in actual_df.iterrows():
        for col, value in expected_data.items():
            assert row[col] == value
