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


# default rcvd date to the lodge date, if the row doesn't have a rcvd date
def _set_default_rcvd_date(df: pd.DataFrame) -> pd.Series:
    df.loc[
        (df["c_lodge_date"] != "")
        & df["c_lodge_date"].notna()
        & (df["c_rcvd_date"].isna() | (df["c_rcvd_date"] == "")),
        "c_rcvd_date",
    ] = df["c_lodge_date"]

    return df["c_rcvd_date"]


# see IN-763, table 1
_mappings = [
    {
        "default_cols": {
            "status": None,
            "reviewstatus": None,
            "c_rcvd_date": _set_default_rcvd_date,
        }
    },
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
    # rule 5 from IN-1136
    # 'N' rev stat with rcvd date, lodge date and review date set
    # -> status="LODGED", reviewstatus=NULL
    {
        "criteria": [
            'c_rev_stat == "N"',
            {"any_set": _rcvd_date_cols},
            {"any_set": ["c_lodge_date"]},
            {"any_set": ["c_review_date"]},
        ],
        "output_cols": {"status": "LODGED", "reviewstatus": None},
    },
    # table 1, row 7
    {
        "criteria": [
            'c_rev_stat == "I"',
            {"any_set": _rcvd_date_cols},
            {"any_set": ["c_lodge_date"]},
        ],
        "output_cols": {"status": "INCOMPLETE", "reviewstatus": "NO_REVIEW"},
    },
    # rule 3 from IN-1136
    # 'R' rev stat with rcvd date and lodge date but no review date
    # -> status="OVERDUE", reviewstatus=NULL
    {
        "criteria": [
            'c_rev_stat == "R"',
            {"any_set": _rcvd_date_cols},
            {"any_set": ["c_lodge_date"]},
            {"all_unset": ["c_review_date"]},
        ],
        "output_cols": {"status": "OVERDUE", "reviewstatus": None},
    },
    # rule 8 from IN-1136
    # 'R' Rev Stat with Rcvd Date but no Lodge Date or Review Date
    # -> status="DUE", reviewstatus="STAFF_REFERRED"
    {
        "criteria": [
            'c_rev_stat == "R"',
            {"any_set": _rcvd_date_cols},
            {"all_unset": ["c_lodge_date"]},
            {"all_unset": ["c_review_date"]},
        ],
        "output_cols": {"status": "DUE", "reviewstatus": "STAFF_REFERRED"},
    },
    # rule 2 from IN-1136
    # 'R' rev stat with no rcvd date and no lodge date and no review date
    # -> status="OVERDUE", reviewstatus=NULL
    {
        "criteria": [
            'c_rev_stat == "R"',
            {"all_unset": _rcvd_date_cols},
            {"all_unset": ["c_lodge_date"]},
            {"all_unset": ["c_review_date"]},
        ],
        "output_cols": {"status": "OVERDUE", "reviewstatus": None},
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
    # rule 4 from IN-1136
    # 'S' rev stat with null rcvd date and null lodge date
    # -> status="OVERDUE", reviewstatus=NULL
    {
        "criteria": [
            'c_rev_stat == "S"',
            {"all_unset": _rcvd_date_cols},
            {"all_unset": ["c_lodge_date"]},
        ],
        "output_cols": {"status": "OVERDUE", "reviewstatus": None},
    },
    # rule 6 from IN-1136
    # 'S' rev stat with a rcvd date and no lodge date and no review date
    # -> status="DUE", reviewstatus="STAFF_REFERRED"
    {
        "criteria": [
            'c_rev_stat == "S"',
            {"any_set": _rcvd_date_cols},
            {"all_unset": ["c_lodge_date"]},
            {"all_unset": ["c_review_date"]},
        ],
        "output_cols": {"status": "DUE", "reviewstatus": "STAFF_REFERRED"},
    },
    # rule 7 from IN-1136
    # 'G' rev stat with rcvd date and lodge date and no review date
    # -> status="LODGED", reviewstatus="STAFF_REFERRED"
    {
        "criteria": [
            'c_rev_stat == "G"',
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
    # table 1, row 11 / rule 9 from IN-1136
    {
        "criteria": ['c_rev_stat == "X"'],
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
}
