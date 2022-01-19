# variables referenced in mapping criteria below
_local_vars = {}

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

# used to check whether any sent date has been set
_sent_date_cols = ["c_sent1", "c_sent2", "c_sent3", "c_sent4", "c_sent5", "c_sent6"]

_all_date_cols = (
    _rcvd_date_cols
    + _sent_date_cols
    + ["c_lodge_date", "c_review_date", "c_revise_date", "c_followup_date"]
)

# datatypes for aliased columns
_aliased_column_datatypes = {
    "c_rev_stat": {"data_type": "string"},
    "c_further_code": {"data_type": "string"},
}
for date_col in _all_date_cols:
    _aliased_column_datatypes[date_col] = {"data_type": "date"}

# see IN-763, tables 1 and 2
_mappings = [
    {"default_cols": {"lodgedstatus": None}},
    # arld rule 1.6 (table 1, row 6)
    {
        "criteria": [
            'c_rev_stat == "N"',
            {"any_set": _rcvd_date_cols},
            {"any_set": ["c_lodge_date"]},
            {"all_unset": ["c_review_date"]},
        ],
        "output_cols": {"lodgedstatus": "ACKNOWLEDGED"},
    },
    # arld rule 1.7 (table 1, row 7)
    {
        "criteria": [
            'c_rev_stat == "I"',
            {"any_set": _rcvd_date_cols},
            {"any_set": ["c_lodge_date"]},
            {"all_unset": ["c_review_date"]},
        ],
        "output_cols": {"lodgedstatus": "INCOMPLETE"},
    },
    # arld rule 1.8 (table 1, row 8)
    {
        "criteria": [
            'c_rev_stat == "S"',
            {"any_set": _rcvd_date_cols},
            {"any_set": ["c_lodge_date"]},
        ],
        "output_cols": {"lodgedstatus": "REFERRED_FOR_REVIEW"},
    },
    # arld rule 1.9 (table 1, row 9)
    {
        "criteria": [
            'c_rev_stat.isin(["R", "G", "M"])',
            {"any_set": _rcvd_date_cols},
            {"any_set": ["c_lodge_date"]},
            {"any_set": ["c_review_date"]},
        ],
        "output_cols": {"lodgedstatus": "REFERRED_FOR_REVIEW"},
    },
    # arld rule 2.1 (table 2, row 1)
    {
        "criteria": [
            {"any_set": ["c_revise_date"]},
            'c_further_code.isin(["2", "3", "4"])',
            {"all_unset": _rcvd_date_cols},
            {"all_unset": _sent_date_cols},
            {"any_set": ["c_followup_date"]},
        ],
        "output_cols": {"lodgedstatus": "INCOMPLETE"},
    },
    # arld rule 2.2 (table 2, row 2)
    {
        "criteria": [
            {"any_set": ["c_revise_date"]},
            'c_further_code.isin(["2", "3", "4"])',
            {"any_set": _rcvd_date_cols},
            {"all_unset": _sent_date_cols},
            {"any_set": ["c_followup_date"]},
        ],
        "output_cols": {"lodgedstatus": "INCOMPLETE"},
    },
    # arld rule 2.3 (table 2, row 3)
    {
        "criteria": [
            {"any_set": ["c_revise_date"]},
            'c_further_code.isin(["1", "8"])',
            {"all_unset": _rcvd_date_cols},
            {"any_set": _sent_date_cols},
            {"all_unset": ["c_followup_date"]},
        ],
        "output_cols": {"lodgedstatus": "REFERRED_FOR_REVIEW"},
    },
    # arld rule 2.4 (table 2, row 4)
    {
        "criteria": [
            {"any_set": ["c_revise_date"]},
            'c_further_code.isin(["1", "8"])',
            {"any_set": _rcvd_date_cols},
            {"any_set": _sent_date_cols},
            {"all_unset": ["c_followup_date"]},
        ],
        "output_cols": {"lodgedstatus": "REFERRED_FOR_REVIEW"},
    },
    # arld rule 2.5 (table 2, row 5)
    {
        "criteria": [
            {
                "all_unset": ["c_further_code", "c_revise_date", "c_followup_date"]
                + _rcvd_date_cols
                + _sent_date_cols
            }
        ],
        "output_cols": {"lodgedstatus": "REFERRED_FOR_REVIEW"},
    },
]


TABLE_TRANSFORM_ANNUAL_REPORT_LODGING_DETAILS = {
    "datatypes": _aliased_column_datatypes,
    "mappings": _mappings,
    "local_vars": _local_vars,
}
