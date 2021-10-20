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
    However, datatypes are probably not going to be what you want.

    The keys of calculated_fields specify the calculation.
    'current_date' and 'uuid4' are self-explanatory.

    'calculate_date' has a more involved format:

        'calculate_date:<base field>(+|-)<days>|<optional weekend adjustment>'

    <base field> is a date field in the dataframe to base the calculation on

    (+|-)<days> is the number of days to add/subtract from the base

    <optional weekend adjustment> is how to adjust the calculated date
    if it falls on a weekend, and is one of:
        * previous-working-day
        * next-working-day
    These refer to the working day before or after the weekend of the calculated
    date respectively.

    For example:

        'calculate_date:reportingperiodenddate+21|next-working-day': ['duedate']

    means calculate the duedate field from the reportingperiodenddate field + 21 days;
    if the result falls on a weekend, select the next working day after that
    weekend instead.

    If this adjustment isn't needed:

        'calculate_date:reportingperiodenddate+21': ['duedate']

    just sets duedate to 21 days after reportingperiodenddate.

    If the base field has no date, no calculation is performed, and the fields
    calculated from it are untouched.

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
