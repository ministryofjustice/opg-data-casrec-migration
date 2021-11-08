"""
Table transforms are applied to convert one or more columns in the source
CSV into one or more columns in the target table. At the point of transformation,
datatypes have been applied to the source CSV, so date comparisons etc. can be
used in the transforms.

Each table transform is defined in a file which exports a constant representing
the table transform configuration, as follows:

{
    'datatypes': <dict of column name to datatype pairs>,
    'mappings': <list of mapping dicts>,
    'local_vars': <dict of variables interpolated into mapping dicts>
}

# datatypes

Columns in the dataframe are cast to the specified datatypes before the mappings
are applied. This dict maps from column name to datatype; datatype is one of
the strings recognised

# mappings

Each mapping dict in this list specifies either:

* default_cols: default values for the specified columns before
  more-specific transforms are applied; this ensures these columns
  get a value in rows which don't match the more-specific transforms

* a dict with 'criteria' (and-ed together to construct a dataframe query)
  and 'output_cols' keys.

  criteria may be inline clauses for the dataframe query, or a combination
  of operator (see below) with a list of fields:

  * all_null: True if all the specified columns have null (or NaT) values
  * any_not_null: True if one or more of the specified columns are not null/NaT

  output_cols: columns to set on a row with specified values if criteria are met

  any '@' variables in these criteria must be set in the local_vars dict and
  passed into the apply_table_transformation() function

# local_vars

Variables which are to be interpolated into mappings when constructing queries on an
annual_report_logs dataframe. These are referenced using the pandas "@" syntax
within the mappings list.
"""

import logging
import numpy as np
import pandas as pd
from datetime import datetime

from transform_data.apply_datatypes import apply_datatypes
from transform_data.table_transforms_annual_report_logs import TABLE_TRANSFORM_ANNUAL_REPORT_LOGS


log = logging.getLogger('root')


def apply_table_transformation(df: pd.DataFrame, mapping: dict, local_vars: dict={}) -> pd.DataFrame:
    """
    Apply default columns from mapping, or check criteria in mapping and set
    output columns if criteria are met

    :param df: dataframe to transform in place
    :param mapping: dict; will either set default_cols, or specify criteria to test against the
        dataframe + output columns to set if criteria met
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
        log.debug(f'Table transform query: {query} => {output_cols}')

        try:
            df.loc[df.eval(query, local_dict=local_vars), output_cols.keys()] = output_cols.values()
        except pd.core.computation.ops.UndefinedVariableError as e:
            log.error('ERROR creating query for table transform; likely missing local_vars key')
            raise(e)

    return df


def _get_annual_report_lodging_details_local_vars() -> pd.DataFrame:
    """
    Get variables which are to be interpolated into mappings when constructing queries on an
    annual_report_lodging_details dataframe.

    :return: dict of local variables to interpolate into mapping criteria queries
    """
    return {}


# definition of transforms which may be applied to tables
#
# this maps from transform names (as used in mapping spreadsheets) to datatypes, mappings
# and local variables to be applied, typically specified in imported files
TRANSFORMS = {
    'set_annual_report_logs_status': TABLE_TRANSFORM_ANNUAL_REPORT_LOGS,
    'set_annual_report_lodging_details_status': {
        'datatypes': {},
        'mappings': [],
        'local_vars': _get_annual_report_lodging_details_local_vars()
    }
}


def process_table_transformations(df: pd.DataFrame, table_transforms: dict) -> pd.DataFrame:
    """
    Apply table-level transforms to a dataframe

    :param df: dataframe to apply table-level transforms to
    :param table_transforms: dict; Table-level transforms to be applied to the table. This is a
        map from transform name to parameters for that transform, derived from the table
        definitions JSON (which itself comes from the spreadsheets). The parameters are
        primarily informational and used to define the columns required in the initial
        dataframe and hint at which columns will be affected by it, and are not (currently)
        used during transformation.
    :return: dataframe after transforms have been applied
    """
    for transform_name, _ in table_transforms.items():
        transform = TRANSFORMS.get(transform_name)
        if transform is None:
            raise KeyError(f'No table transform named {transform_name} exists')

        # apply datatypes to df (if specified); datetimes which fail to parse
        # are coerced to NaT
        if 'datatypes' in transform:
            df = apply_datatypes(transform['datatypes'], df, datetime_errors='coerce')

        # call mapping function
        log.debug(f'Applying table transform {transform_name}')

        mappings = transform['mappings']
        local_vars = transform['local_vars']

        for mapping in mappings:
            df = apply_table_transformation(df, mapping, local_vars)

    return df
