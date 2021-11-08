"""
Table transforms are applied to convert one or more columns in the source
CSV into one or more columns in the target table. At the point of transformation,
datatypes have been applied to the source CSV, so date comparisons etc. can be
used in the transforms.
"""

import logging
import numpy as np
import pandas as pd
from datetime import datetime

from transform_data.apply_datatypes import apply_datatypes


log = logging.getLogger('root')


def _apply_mapping(df: pd.DataFrame, mapping: list, local_vars: dict={}) -> pd.DataFrame:
    """
    Apply default columns from mapping, or check criteria in mapping and set
    output columns if criteria are met

    :param df: dataframe to transform in place
    :param mapping: dict; dict object, which will either set default_cols
        or specify criteria to test against the dataframe + output columns to set if met
    :param local_vars: dict; local variables which will be interpolated into the
        criteria in the mappings
    :return: dataframe
    """
    if 'default_cols' in mapping:
        for output_col, value in mapping['default_cols'].items():
            df[output_col] = value

    elif 'criteria' in mapping:
        parsed = []
        for condition in mapping['criteria']:
            if isinstance(condition, str):
                parsed.append(condition)

            elif isinstance(condition, dict):
                if 'all_null' in condition:
                    # isnull() also returns True for NaT fields
                    parsed += list(map(lambda field: f'{field}.isnull()', condition['all_null']))

                elif 'any_not_null' in condition:
                    # OR clause which checks for at least one column which is not null
                    clauses = map(lambda field: f'{field}.notnull()', condition['any_not_null'])
                    parsed.append('((' + ') | ('.join(clauses) + '))')

        query = '(' + ') & ('.join(parsed) + ')'

        # find matching rows and set column values
        output_cols = mapping['output_cols']
        log.verbose(f'Table transform query: {query} => {output_cols}')

        try:
            df.loc[df.eval(query, local_dict=local_vars), output_cols.keys()] = output_cols.values()
        except pd.core.computation.ops.UndefinedVariableError as e:
            log.error('ERROR creating query for table transform; likely missing local_vars key')
            raise(e)

    return df


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

# default_cols: specifies default values for columns mentioned before
#     more-specific transforms are applied; this ensures these fields
#     get a value in rows which don't match the more-specific transforms
#
# criteria are and-ed together
# all_null: True if all the specified columns have null (or NaT) values
# any_not_null: True if one or more of the specified columns are not null/NaT
#
# output_cols: columns to set on a row with specified values if criteria are met
#
# any '@' variables in these criteria must be set in the local_vars dict and
# passed into the _apply_mappings() function
ANNUAL_REPORT_LOGS_STATUS_MAPPINGS = [
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


def _get_annual_report_logs_local_vars() -> pd.DataFrame:
    """
    Get variables which are to be interpolated into mappings when constructing queries on the dataframe.

    :return: dict of local variables to interpolate into mapping criteria queries
    """

    # construct variables which are mentioned in the mappings
    now = np.datetime64(datetime.now().strftime('%Y-%m-%d'))

    # now < End Date + X working days
    #   is equivalent to
    # End Date > now - X working days
    #
    # roll='forward' means to choose the next working day if the offset
    # resolves to a day on the weekend
    return {
        'now': now,
        'fifteen_working_days_ago': np.busday_offset(now, -15, roll='forward'),
        'seventy_one_working_days_ago': np.busday_offset(now, -71, roll='forward')
    }


def _get_annual_report_lodging_details_local_vars() -> pd.DataFrame:
    """
    Use params['source_cols'] as source data to generate status values for columns in
    params['target_cols'].

    :param df: dataframe for annual_report_lodging_details table
    :param params: dict in format
        {'source_cols': <str[] of source column names>, 'target_cols': <str[] of target column names>}
    """
    return {}


# map from function names (as used in mapping spreadsheets) to transform function and
# datatypes to apply
TABLE_TRANSFORMS = {
    'set_annual_report_logs_status': {
        'datatypes': _aliased_column_datatypes,
        'mappings': ANNUAL_REPORT_LOGS_STATUS_MAPPINGS,
        'local_vars': _get_annual_report_logs_local_vars()
    },
    'set_annual_report_lodging_details_status': {
        'datatypes': _aliased_column_datatypes,
        'mappings': [],
        'local_vars': _get_annual_report_lodging_details_local_vars()
    }
}


def process_table_transformations(df: pd.DataFrame, table_transforms: dict) -> pd.DataFrame:
    """
    Apply table-level transforms to a dataframe

    :param df: dataframe to apply table transforms to
    :param table_transforms: dict; map from function name to parameters
        for that transform; the transform is composed of an (optional) dict
        of datatypes to apply to the dataframe, and (mandatory) mappings list and
        local_vars dict
    :return: dataframe after transforms have been applied
    """
    for function_name, params in table_transforms.items():
        transform = TABLE_TRANSFORMS.get(function_name)
        if transform is None:
            raise KeyError(f'No transform function named {function_name} exists')

        # apply datatypes to df (if specified); datetimes which fail to parse
        # are coerced to NaT
        if 'datatypes' in transform:
            df = apply_datatypes(transform['datatypes'], df, datetime_errors='coerce')

        # call mapping function
        log.verbose(f'Applying table transform {function_name}')

        mappings = transform['mappings']
        local_vars = transform['local_vars']

        for mapping in mappings:
            df = _apply_mapping(df, mapping, local_vars)

    return df
