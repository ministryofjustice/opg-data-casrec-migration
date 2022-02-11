# see IN-1089
_mappings = [
    {
        "default_cols": {
            "visitsubtype": None,
        }
    },
    {
        "criteria": [
            "c_req_by.isin([1, 2, 4, 5, 6, 7])",
            "c_report_type == 1",
        ],
        "output_cols": {"visitsubtype": "VST-LAY"},
    },
    {
        "criteria": [
            "c_req_by.isin([1, 2, 4, 5, 6, 7])",
            "c_report_type == 2",
        ],
        "output_cols": {"visitsubtype": "VST-HW"},
    },
    {
        "criteria": [
            "c_req_by.isin([1, 2, 4, 5, 6, 7])",
            "c_report_type == 3",
        ],
        "output_cols": {"visitsubtype": "VST-MED"},
    },
    {
        "criteria": [
            "c_req_by == 3",
            "c_report_type.isin([1, 2])",
        ],
        "output_cols": {"visitsubtype": "VST-DEP"},
    },
    {
        "criteria": [
            "c_req_by == 3",
            "c_report_type == 3",
        ],
        "output_cols": {"visitsubtype": "VST-MLPA"},
    },
    {
        "criteria": [
            "c_req_by.isin([8, 9, 10, 11, 12, 13, 14])",
            "c_report_type.isin([1, 2, 3])",
        ],
        "output_cols": {"visitsubtype": "VST-PRO"},
    },
]


TABLE_TRANSFORM_VISITS = {
    "datatypes": {
        "c_req_by": {"data_type": "int"},
        "c_report_type": {"data_type": "int"},
    },
    "mappings": _mappings,
    "local_vars": {},
}
