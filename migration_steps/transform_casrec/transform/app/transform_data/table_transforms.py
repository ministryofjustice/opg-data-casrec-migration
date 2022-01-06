"""
Table transforms are applied to convert one or more columns in the source
CSV into one or more columns in the target table.

Each table transform is defined in a file which exports a constant representing
the table transform configuration, as follows:

{
    'datatypes': <dict of column name to datatype pairs>,
    'mappings': <list of mapping dicts>,
    'local_vars': <dict of variables interpolated into mapping dicts>
}

# datatypes

Columns in the dataframe are cast to the specified datatypes before the mappings
are applied. This dict maps from column name to {'data_type': <type>}; datatype is one of
the strings recognised by apply_datatypes().

Example:

{
    'c_revise_date': {'data_type': 'date'},
    'c_rev_stat': {'data_type': 'str'}
}

# mappings

Each mapping dict in this list specifies either:

* default_cols: default values for the specified columns before
  more-specific transforms are applied; this ensures these columns
  get a value in rows which don't match the more-specific transforms.

  This is specified as a dictionary:

  {
    '<column name>': <value or callable>
  }

  If a value, all rows in that column get that value, regardless of
  whether they already have a value. If a callable, should be a
  function which takes a single argument (the whole dataframe) and returns
  a pandas.Series. The column within the dataframe is then set to this
  returned series. This allows for setting more complex defaults
  which don't override all the values in the column.

  Usually, this should be the first item in the mappings list, especially
  if later mappings rely on values which have been set up by default_cols.

* a dict with 'criteria' (and-ed together to construct a dataframe query)
  and 'output_cols' keys:

  criteria: may be inline clauses for the dataframe query, or an
  operator with a list of column names, as follows:

  * all_unset: True if all the specified columns have null (or NaT or '') values
  * any_set: True if one or more of the specified columns are not null/NaT/''

  any '@' variables in the criteria must be set in the local_vars dict

  output_cols: columns to set on a row with specified values if criteria are met

# local_vars

Variables which are to be interpolated into mappings when constructing queries on an
annual_report_logs dataframe. These are referenced using the pandas "@" syntax
within criteria in the mappings list.

Example:

{
    'now': <instance of numpy.datetime64>
}
"""

import logging
import pandas as pd

from transform_data.apply_datatypes import apply_datatypes
from transform_data.table_transforms_annual_report_logs import (
    TABLE_TRANSFORM_ANNUAL_REPORT_LOGS,
)
from transform_data.table_transforms_annual_report_lodging_details import (
    TABLE_TRANSFORM_ANNUAL_REPORT_LODGING_DETAILS,
)
from transform_data.table_transforms_cases import TABLE_TRANSFORM_CASES

log = logging.getLogger("root")


# definition of default set of transforms which may be applied to tables
#
# this maps from transform names (as used in mapping spreadsheets) to datatypes, mappings
# and local variables to be applied, typically specified in imported modules
DEFAULT_TRANSFORMS = {
    "set_annual_report_logs_status": TABLE_TRANSFORM_ANNUAL_REPORT_LOGS,
    "set_annual_report_lodging_details_status": TABLE_TRANSFORM_ANNUAL_REPORT_LODGING_DETAILS,
    "set_cases_orderstatus": TABLE_TRANSFORM_CASES,
}


# raised when table transform fails for some reason
class TableTransformException(Exception):
    pass


def apply_table_transformation(
    df: pd.DataFrame, mapping: dict, local_vars: dict = {}
) -> pd.DataFrame:
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
    if "default_cols" in mapping:
        for output_col, value_or_func in mapping["default_cols"].items():
            if callable(value_or_func):
                df[output_col] = value_or_func(df)
            else:
                df[output_col] = value_or_func

    elif "criteria" in mapping:
        parsed = []
        for condition in mapping["criteria"]:
            if isinstance(condition, str):
                parsed.append(condition)

            elif isinstance(condition, dict):
                if "all_unset" in condition:
                    # all_unset() returns True if all columns have null, NaT or "" values
                    parsed += list(
                        map(
                            lambda field: f'({field}.isnull() | {field} == "")',
                            condition["all_unset"],
                        )
                    )

                elif "any_set" in condition:
                    # OR clause which checks for at least one column which is not null and not ""
                    clauses = map(
                        lambda field: f'({field}.notnull() & {field} != "")',
                        condition["any_set"],
                    )
                    parsed.append("((" + ") | (".join(clauses) + "))")

        query = "(" + ") & (".join(parsed) + ")"

        # find matching rows and set column values
        output_cols = mapping["output_cols"]
        log.debug(f"Table transform query: {query} => {output_cols}")

        try:
            # cast to list is required as values() returns a dict view which is not treated as expected
            # by pandas
            df.loc[df.eval(query, local_dict=local_vars), list(output_cols)] = list(
                output_cols.values()
            )
        except pd.core.computation.ops.UndefinedVariableError as e:
            log.error(
                "ERROR creating query for table transform; likely missing local_vars key"
            )
            raise (e)

    return df


def process_table_transformations(
    df: pd.DataFrame,
    transforms_for_table: dict,
    transform_definitions: dict = DEFAULT_TRANSFORMS,
) -> pd.DataFrame:
    """
    Apply table-level transforms to a dataframe

    :param df: dataframe to apply table-level transforms to
    :param transforms_for_table: dict. Table-level transforms to be applied to this dataframe. This is a
        map from transform name to parameters for that transform, derived from the table
        definitions JSON (which itself comes from the spreadsheets). The parameters are a dict in
        format:
            {
                'source_cols': ['Column Name1', 'Column Name2', ...],
                'target_cols': ['columnname3', 'columnname4', ...]
            }
        'source_cols' is a list of columns in the source data (casrec). This is used to validate
        that the dataframe df has all of the columns required to perform the table transform.
        If the columns do not match, an exception is raised. Note that the source_cols are
        aliased internally, e.g. "Rev Stat" in source_cols equates to c_rev_stat in the dataframe
        under transform.
        'target_cols' is a list of columns set by the table transform, corresponding to Sirius
        column names. The output columns of the mapping are compared to this list; if a column is
        specified as an output of the mapping but not present in target_cols, an exception is raised.
        (A mapping does not have to set a value for all columns in target_cols, but must only set
        columns which are in target_cols.)
    :param transform_definitions: dict. Definitions for valid table transforms; defaults to the
        transforms defined in this module.
    :raises: TableTransformException
    :return: dataframe after transforms have been applied
    """
    for transform_name, params in transforms_for_table.items():
        transform = transform_definitions.get(transform_name)
        if transform is None:
            raise TableTransformException(
                f"No table transform named {transform_name} exists"
            )

        # make the "c_" column names from the source columns specified in the transform config
        source_cols = set(
            map(
                lambda col_name: "c_" + col_name.replace(" ", "_").lower(),
                params["source_cols"],
            )
        )

        # transform should only set columns in this Set
        target_cols = set(params["target_cols"])

        # validate that the source_cols are all present in df
        missing_cols = source_cols - set(df.columns)
        if len(missing_cols) > 0:
            raise TableTransformException(
                f"Dataframe is missing source columns required by {transform_name} "
                f"table transform: {sorted(missing_cols)}"
            )

        # apply datatypes to df (if specified); datetimes which fail to parse
        # are coerced to NaT
        if "datatypes" in transform:
            df = apply_datatypes(transform["datatypes"], df, datetime_errors="coerce")

        # call transformation function with mappings
        log.debug(f"Applying table transform {transform_name}")

        mappings = transform["mappings"]
        local_vars = transform["local_vars"]

        for mapping in mappings:
            # validate that default_cols/output_cols in the mapping are all in target_cols
            if "default_cols" in mapping:
                output_cols = mapping["default_cols"]
            else:
                output_cols = mapping["output_cols"]

            invalid_output_cols = set(output_cols.keys()) - target_cols

            if len(invalid_output_cols) > 0:
                raise TableTransformException(
                    f"Mapping for table transform {transform_name} outputs to column(s) "
                    f"{sorted(invalid_output_cols)} which are not specified "
                    f"in target_cols list {sorted(target_cols)}"
                )

            df = apply_table_transformation(df, mapping, local_vars)

    return df
