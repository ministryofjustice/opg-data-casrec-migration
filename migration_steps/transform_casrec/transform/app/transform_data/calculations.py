import logging

import pandas as pd

from uuid import uuid4
from datetime import datetime


log = logging.getLogger('root')

def do_calculations(
    calculated_fields: dict,
    df: pd.DataFrame,
    now: datetime=datetime.now()
) -> pd.DataFrame:
    """
    Apply calculated values to specified fields in a dataframe.
    Configuration is done in the calculated_fields property of a mapping.

    :param calculated_fields: dictionary of fields to which calculations
        should be applied, where keys are calculations and values
        are dicts each containing a column_name property; for example:
        {
            'current_date': [
                {'column_name': 'todays_date'},
                {'column_name': 'another_date'}
            ],
            'uuid4': [
                {'column_name': 'identifier'}
            ]
        }
    :param df: dataframe to apply calculations to
    :param now: default value to set fields to if current_date calculation
        is being applied
    """
    for calculation, column_names in calculated_fields.items():
        column_names = list(map(lambda item: item['column_name'], column_names))
        log.debug(f'Applying calculation "{calculation}" to columns {column_names}')

        if calculation == "current_date":
            for column_name in column_names:
                df[column_name] = now.strftime("%Y-%m-%d")

        elif calculation == "uuid4":
            for column_name in column_names:
                df[column_name] = df.apply(lambda x: uuid4(), axis=1)

        else:
            # if calculation is unrecognised, current approach is to leave the calculated column alone
            log.error(f'Unrecognised calculation "{calculation}" for columns {column_names}')

    return df
