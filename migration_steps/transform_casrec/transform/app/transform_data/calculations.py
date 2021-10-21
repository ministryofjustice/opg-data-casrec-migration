import logging
import re

import pandas as pd

from uuid import uuid4
from datetime import datetime, timedelta


log = logging.getLogger('root')

# regex for delta_date calculation formulae; matching this regex implicitly
# performs validation on any delta_date calculation formulae
_delta_date_regex = re.compile(
    r"^delta_date:" + \
    r"(?P<base_field>[^\+\-]+)" + \
    r"(?P<operator>[\+\-])" + \
    r"(?P<days>\d+)" + \
    r"\|{0,1}(?P<weekend_adjustment>(previous-working-day|next-working-day){0,1})$"
)

# base_date: date to use as the basis for the delta date
# operator: delta modifier, '+' or '-'
# days: delta number of days
# weekend_adjustment: 'previous-working-day' or 'next-working-day' or None;
#     if None, no adjustment will not be applied
# return: datetime, or None if the base_date is None
def _calculate_date(base_date: pd.Timestamp, operator: str, days: int, weekend_adjustment: str):
    if base_date is None or base_date == '':
        return None

    delta = timedelta(days=days)

    if operator == '+':
        base_date = base_date + delta
    elif operator == '-':
        base_date = base_date - delta

    # Saturday, Sunday = [5, 6]
    weekday = base_date.weekday()
    if weekday in [5, 6]:
        if weekend_adjustment == 'previous-working-day':
            base_date = base_date - timedelta(days=weekday-4)
        elif weekend_adjustment == 'next-working-day':
            base_date = base_date + timedelta(days=7-weekday)

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

    :raise: ValueError if calculation has an invalid format or refers to a
        source column which does not exist
    """
    for calculation, column_names in calculated_fields.items():
        column_names = map(lambda item: item['column_name'], column_names)
        log.debug(f'Applying calculation {calculation} to columns {column_names}')

        if calculation == "current_date":
            for column_name in column_names:
                df[column_name] = now.strftime("%Y-%m-%d")

        elif calculation == "uuid4":
            for column_name in column_names:
                df[column_name] = df.apply(lambda x: uuid4(), axis=1)

        elif calculation.startswith('delta_date'):
            parts = _delta_date_regex.match(calculation)
            if parts is None:
                raise ValueError(f'delta_date calculation "{calculation}" does not match required format')

            base_field = parts.group('base_field')
            operator = parts.group('operator')
            days = int(parts.group('days'))
            weekend_adjustment = parts.group('weekend_adjustment')

            for column_name in column_names:
                try:
                    df[column_name] = df.apply(
                        lambda row: _calculate_date(row[base_field], operator, days, weekend_adjustment),
                        axis=1
                    )
                except KeyError as e:
                    raise ValueError(f'Base field {base_field} in delta_date calculation ' + \
                        f'"{calculation}" does not exist in row')

    return df
