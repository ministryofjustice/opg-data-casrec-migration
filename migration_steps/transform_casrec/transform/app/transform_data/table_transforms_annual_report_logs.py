import numpy as np
import pandas as pd
from datetime import datetime


# variables referenced in mapping criteria below
#
# roll='forward' means to choose the next working day if the offset
# resolves to a day on the weekend
_now = np.datetime64(datetime.now().strftime("%Y-%m-%d"))

_local_vars = {
    "now": _now,
    "fifteen_working_days_ago": np.busday_offset(_now, -15, roll="forward"),
    "seventy_one_working_days_ago": np.busday_offset(_now, -71, roll="forward"),
}

# all received date columns; these are used to check whether there
# is at least one received date
_rcvd_date_cols = [
    "c_rcvd_date",
    "c_rcvd_date1",
    "c_rcvd_date2",
    "c_rcvd_date3",
    "c_rcvd_date4",
    "c_rcvd_date5",
    "c_rcvd_date6",
]

# date columns we check for null values
_all_unset_date_cols = _rcvd_date_cols + ["c_lodge_date", "c_review_date"]

# map of date column names to data type, so we can apply correct datatypes
# for the purpose of doing comparisons below
_aliased_column_datatypes = {
    "c_next_yr": {"data_type": "string"},
    "c_rev_stat": {"data_type": "string"},
}
for date_col in _all_unset_date_cols + ["c_end_date"]:
    _aliased_column_datatypes[date_col] = {"data_type": "date"}

# see IN-763, table 1
_mappings = [
    {"default_cols": {"status": None, "reviewstatus": None}},
    # table 1, row 1
    {
        "criteria": [
            'c_rev_stat == "N"',
            "c_end_date > @now",
            {"all_unset": _all_unset_date_cols},
        ],
        "output_cols": {"status": "PENDING", "reviewstatus": "NO_REVIEW"},
    },
    # table 1, row 2
    {
        "criteria": [
            'c_rev_stat == "N"',
            "c_end_date <= @now",
            "c_end_date > @fifteen_working_days_ago",
            {"all_unset": _all_unset_date_cols},
        ],
        "output_cols": {"status": "DUE", "reviewstatus": "NO_REVIEW"},
    },
    # table 1, row 3
    {
        "criteria": [
            'c_rev_stat == "N"',
            "c_end_date <= @fifteen_working_days_ago",
            "c_end_date > @seventy_one_working_days_ago",
            {"all_unset": _all_unset_date_cols},
        ],
        "output_cols": {"status": "OVERDUE", "reviewstatus": "NO_REVIEW"},
    },
    # table 1, row 4
    {
        "criteria": [
            'c_rev_stat == "N"',
            "c_end_date <= @seventy_one_working_days_ago",
            {"all_unset": _all_unset_date_cols},
        ],
        "output_cols": {"status": "NON_COMPLIANT", "reviewstatus": "NO_REVIEW"},
    },
    # table 1, row 5
    {
        "criteria": [
            'c_rev_stat == "N"',
            {"any_set": _rcvd_date_cols},
            {"all_unset": ["c_lodge_date", "c_review_date"]},
        ],
        "output_cols": {"status": "RECEIVED", "reviewstatus": "NO_REVIEW"},
    },
    # table 1, row 6
    {
        "criteria": [
            'c_rev_stat == "N"',
            {"any_set": _rcvd_date_cols},
            {"any_set": ["c_lodge_date"]},
            {"all_unset": ["c_review_date"]},
        ],
        "output_cols": {"status": "LODGED", "reviewstatus": "NO_REVIEW"},
    },
    # table 1, row 7
    {
        "criteria": [
            'c_rev_stat == "I"',
            {"any_set": _rcvd_date_cols},
            {"any_set": ["c_lodge_date"]},
            {"all_unset": ["c_review_date"]},
        ],
        "output_cols": {"status": "INCOMPLETE", "reviewstatus": "NO_REVIEW"},
    },
    # table 1, row 8
    {
        "criteria": [
            'c_rev_stat == "S"',
            {"any_set": _rcvd_date_cols},
            {"any_set": ["c_lodge_date"]},
            {"all_unset": ["c_review_date"]},
        ],
        "output_cols": {"status": "LODGED", "reviewstatus": "STAFF_REFERRED"},
    },
    # table 1, row 9
    {
        "criteria": [
            'c_rev_stat.isin(["S", "R", "G", "M"])',
            {"any_set": _rcvd_date_cols},
            {"any_set": ["c_lodge_date"]},
            {"any_set": ["c_review_date"]},
        ],
        "output_cols": {"status": "LODGED", "reviewstatus": "REVIEWED"},
    },
    # table 1, row 11
    {
        "criteria": ['c_rev_stat == "X"', {"all_unset": _all_unset_date_cols}],
        "output_cols": {"status": "ABANDONED", "reviewstatus": "NO_REVIEW"},
    },
    # table 1, row 12
    {
        "criteria": [
            {"all_unset": ["c_rev_stat"]},
            "c_end_date > @now",
            {"all_unset": ["c_review_date"]},
            'c_next_yr == "Y"',
        ],
        "output_cols": {"status": "PENDING", "reviewstatus": "STAFF_PRESELECTED"},
    },
]


TABLE_TRANSFORM_ANNUAL_REPORT_LOGS = {
    "datatypes": _aliased_column_datatypes,
    "mappings": _mappings,
    "local_vars": _local_vars,
    "match_once": False,
}
