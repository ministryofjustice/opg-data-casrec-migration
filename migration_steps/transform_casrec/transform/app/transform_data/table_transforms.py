import logging
import pandas as pd


log = logging.getLogger('root')

def _set_annual_report_logs_status(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    """
    Use params['source_cols'] as source data to generate status values for columns in
    params['target_cols'].

    :param df: dataframe for annual_report_logs table
    :param params: dict in format
        {'source_cols': <str[] of source column names>, 'target_cols': <str[] of target column names>}
    :return: dataframe
    """
    return df

def _set_annual_report_lodging_details_status(df: pd.DataFrame, params: dict) -> pd.DataFrame:
    """
    Use params['source_cols'] as source data to generate status values for columns in
    params['target_cols'].

    :param df: dataframe for annual_report_lodging_details table
    :param params: dict in format
        {'source_cols': <str[] of source column names>, 'target_cols': <str[] of target column names>}
    """
    return df


# map from function names (as used in mapping spreadsheets) to transform functions
TABLE_TRANSFORMS = {
    'set_annual_report_logs_status': _set_annual_report_logs_status,
    'set_annual_report_lodging_details_status': _set_annual_report_lodging_details_status,
}


def process_table_transformations(df: pd.DataFrame, table_transforms: dict) -> pd.DataFrame:
    """
    Apply table-level transforms to a dataframe

    :param df: dataframe to apply table transforms to
    :param table_transforms: dict; map from function name to parameters
        for that function; the function name is used to find a function
        which is then passed the dataframe and the parameters
    :return: dataframe after transforms have been applied
    """
    for function_name, params in table_transforms.items():
        fn = TABLE_TRANSFORMS.get(function_name)
        if fn is None:
            raise KeyError(f'No transform function named {function_name} exists')
        log.verbose(f'Applying table transform {fn}')
        df = fn(df, params)

    return df