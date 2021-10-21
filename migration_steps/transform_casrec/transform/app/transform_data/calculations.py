import logging
import re

import pandas as pd

from uuid import uuid4
from datetime import datetime, timedelta


log = logging.getLogger('root')

# regex for delta_date calculation formulae
_delta_date_regex = re.compile(
    r"^delta_date:" + \
    r"(?P<base_field>[^\+\-]+)" + \
    r"(?P<operator>[\+\-])" + \
    r"(?P<days>\d+)" + \
    r"\|{0,1}(?P<weekend_adjustment>[^\|]*)$"
)

# base_date: pd.Timestamp
# operator: delta modifier, '+' or '-'; if neither of these, return None
# days: str; delta number of days; if not parseable as an int, return None
# weekend_adjustment: 'previous-working-day' or 'next-working-day' or None;
#     if None, no adjustment will not be applied; if any other value, return None
# return: datetime or None
def _calculate_date(base_date: pd.Timestamp, operator: str, days: str, weekend_adjustment: str):
    if base_date is None or base_date == '':
        log.error('Invalid base date value for calculation of date delta')
        return None

    try:
        delta = timedelta(days=int(days))
    except TypeError:
        log.error(f'Invalid delta for number of days: {days}')
        return None

    if operator == '+':
        base_date = base_date + delta
    elif operator == '-':
        base_date = base_date - delta
    else:
        log.error(f'Invalid delta operator: {operator}')
        return None

    # Saturday, Sunday = [5, 6]
    weekday = base_date.weekday()
    if weekday in [5, 6]:
        if weekend_adjustment == 'previous-working-day':
            base_date = base_date - timedelta(days=weekday-4)
        elif weekend_adjustment == 'next-working-day':
            base_date = base_date + timedelta(days=7-weekday)
        elif weekend_adjustment is not None:
            log.error(f'Weekend adjustment has invalid value: {weekend_adjustment}')
            return None

    return base_date

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

    'delta_date' has a more involved format:

        'delta_date:<base field>(+|-)<days>|<(optional) weekend adjustment>'

    <base field> is a date field in the dataframe to base the calculation on

    (+|-)<days> is the number of days to add/subtract from the base

    <(optional) weekend adjustment> is how to adjust the calculated date
    if it falls on a weekend, and is one of:
        * previous-working-day
        * next-working-day
    These refer to the working day before or after the weekend of the calculated
    date respectively.

    For example:

        'delta_date:reportingperiodenddate+21|next-working-day': ['duedate']

    means calculate the duedate field from the reportingperiodenddate field + 21 days;
    if the result falls on a weekend, select the next working day after that
    weekend instead.

    If this adjustment isn't needed:

        'delta_date:reportingperiodenddate+21': ['duedate']

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

        elif calculation.startswith('delta_date'):
            parts = _delta_date_regex.match(calculation)

            base_field = parts.group('base_field')
            operator = parts.group('operator')
            days = parts.group('days')
            weekend_adjustment = parts.group('weekend_adjustment')

            for column_name in column_names:
                df[column_name] = df.apply(
                    lambda row: _calculate_date(row[base_field], operator, days, weekend_adjustment),
                    axis=1
                )

    return df
