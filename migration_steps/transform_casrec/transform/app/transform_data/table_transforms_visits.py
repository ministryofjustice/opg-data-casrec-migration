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
]


TABLE_TRANSFORM_VISITS = {
    "datatypes": {
        "c_req_by": {"data_type": "int"},
        "c_report_type": {"data_type": "int"},
    },
    "mappings": _mappings,
    "local_vars": {},
}
