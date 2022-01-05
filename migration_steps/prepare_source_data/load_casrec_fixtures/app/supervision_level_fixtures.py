"""
Dynamic fixtures for the casrec order table for testing supervision level
"""

SUPERVISION_LEVEL_FIXTURES = {
    "source_query": 'SELECT "Case" FROM {schema}.order WHERE "Case" = \'{case}\'',
    # set an account's fields to fixture values
    "update_query": "UPDATE {schema}.order SET {set_clause} WHERE {where_clause}",
    "updates": [
        {
            # General / High
            "source_criteria": {"case": "10369939"},
            "set": {"Ord Risk Lvl": "1"},
        },
        {
            # General / High
            "source_criteria": {"case": "94087154"},
            "set": {"Ord Risk Lvl": "2"},
        },
        {
            # General / High
            "source_criteria": {"case": "13581220"},
            "set": {"Ord Risk Lvl": "2A"},
        },
        {
            # Minimal / Low
            "source_criteria": {"case": "97432184"},
            "set": {"Ord Risk Lvl": "3"},
        },
        {
            # Unknown
            "source_criteria": {"case": "10424217"},
            "set": {"Ord Risk Lvl": ""},
        },
    ],
}
