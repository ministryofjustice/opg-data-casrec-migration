import pandas as pd

from uuid import uuid4
from datetime import datetime


def do_calculations(
    calculated_fields: dict,
    df: pd.DataFrame,
    now: datetime=datetime.now()
) -> pd.DataFrame:
    """
    Apply calculated values to specified fields in a dataframe.
    Configuration is done in the calculated_fields property of a mapping.
    Note that the dataframe has already been populated by the time
    do_calculations() is called (see transform.py), so calculations
    can make use of values in other fields, and not just casrec fields.

    :param calculated_fields: dictionary of fields to which calculations
        should be applied, where keys are calculations and values
        are column names; for example:
        {
            'current_date': ['todays_date', 'another_date'],
            'uuid4': ['identifier']
        }
    :param df: dataframe to apply calculations to
    :param now: default value to set fields to if current_date calculation
        is being applied
    """
    for calculation, column_names in calculated_fields.items():
        if calculation == "current_date":
            for column_name in column_names:
                df[column_name] = now.strftime("%Y-%m-%d")

        elif calculation == "uuid4":
            for column_name in column_names:
                df[column_name] = df.apply(lambda x: uuid4(), axis=1)

    return df
