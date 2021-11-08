import numpy as np
import pandas as pd
from datetime import datetime


# variables referenced in mapping criteria below
#
# roll='forward' means to choose the next working day if the offset
# resolves to a day on the weekend
_now = np.datetime64(datetime.now().strftime('%Y-%m-%d'))

_local_vars = {
    'now': _now,
    'fifteen_working_days_ago': np.busday_offset(_now, -15, roll='forward'),
    'seventy_one_working_days_ago': np.busday_offset(_now, -71, roll='forward')
}

# all received date columns; these are used to check whether there
# is at least one received date
_rcvd_date_cols = [
    'c_rcvd_date',
    'c_rcvd_date1',
    'c_rcvd_date2',
    'c_rcvd_date3',
    'c_rcvd_date4',
    'c_rcvd_date5',
    'c_rcvd_date6'
]

# date columns we check for null values
_all_null_date_cols = _rcvd_date_cols + [
    'c_lodge_date',
    'c_review_date'
]

# map of date column names to data type, so we can apply correct datatypes
# to dates for the purpose of doing comparisons below
_aliased_column_datatypes = {}
for date_col in _all_null_date_cols + ['c_end_date']:
    _aliased_column_datatypes[date_col] = {'data_type': 'date'}

_mappings = [
    {
        'default_cols': {
            'status': None,
            'reviewstatus': None
        }
    },
    {
        'criteria': [
            'c_rev_stat == "N"',
            'c_end_date > @now',
            {'all_null': _all_null_date_cols}

        ],
        'output_cols': {
            'status': 'PENDING',
            'reviewstatus': 'NO_REVIEW'
        }
    },
    {
        'criteria': [
            'c_rev_stat == "N"',
            'c_end_date <= @now',
            'c_end_date > @fifteen_working_days_ago',
            {'all_null': _all_null_date_cols}
        ],
        'output_cols': {
            'status': 'DUE',
            'reviewstatus': 'NO_REVIEW'
        }
    },
    {
        'criteria': [
            'c_rev_stat == "N"',
            'c_end_date <= @fifteen_working_days_ago',
            'c_end_date > @seventy_one_working_days_ago',
            {'all_null': _all_null_date_cols}
        ],
        'output_cols': {
            'status': 'OVERDUE',
            'reviewstatus': 'NO_REVIEW'
        }
    },
    {
        'criteria': [
            'c_rev_stat == "N"',
            'c_end_date <= @seventy_one_working_days_ago',
            {'all_null': _all_null_date_cols}
        ],
        'output_cols': {
            'status': 'NON_COMPLIANT',
            'reviewstatus': 'NO_REVIEW'
        }
    },
    {
        'criteria': [
            'c_rev_stat == "N"',
            {'any_not_null': _rcvd_date_cols},
            {'all_null': ['c_lodge_date', 'c_review_date']}
        ],
        'output_cols': {
            'status': 'RECEIVED',
            'reviewstatus': 'NO_REVIEW'
        }
    },
    {
        'criteria': [
            'c_rev_stat == "N"',
            {'any_not_null': _rcvd_date_cols},
            {'any_not_null': ['c_lodge_date']},
            {'all_null': ['c_review_date']}
        ],
        'output_cols': {
            'status': 'LODGED',
            'reviewstatus': 'NO_REVIEW'
        }
    },
    {
        'criteria': [
            'c_rev_stat == "I"',
            {'any_not_null': _rcvd_date_cols},
            {'any_not_null': ['c_lodge_date']},
            {'all_null': ['c_review_date']}
        ],
        'output_cols': {
            'status': 'INCOMPLETE',
            'reviewstatus': 'NO_REVIEW'
        }
    },
    {
        'criteria': [
            'c_rev_stat == "S"',
            {'any_not_null': _rcvd_date_cols},
            {'any_not_null': ['c_lodge_date']},
            {'all_null': ['c_review_date']}
        ],
        'output_cols': {
            'status': 'LODGED',
            'reviewstatus': 'STAFF_REFERRED'
        }
    },
    {
        'criteria': [
            'c_rev_stat.isin(["S", "R", "G", "M"])',
            {'any_not_null': _rcvd_date_cols},
            {'any_not_null': ['c_lodge_date']},
            {'any_not_null': ['c_review_date']}
        ],
        'output_cols': {
            'status': 'LODGED',
            'reviewstatus': 'REVIEWED'
        }
    },
    {
        'criteria': [
            'c_rev_stat == "X"',
            {'all_null': _all_null_date_cols}
        ],
        'output_cols': {
            'status': 'ABANDONED',
            'reviewstatus': 'NO_REVIEW'
        }
    }
]


TABLE_TRANSFORM_ANNUAL_REPORT_LOGS = {
    'datatypes': _aliased_column_datatypes,
    'mappings': _mappings,
    'local_vars': _local_vars
}
