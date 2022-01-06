"""
Dynamic fixtures for the casrec order table for testing deputy clients
"""

CLIENT_ORDERS_FIXTURES = {
    "source_query": 'SELECT "Case" FROM {schema}.order WHERE "Case" = \'{case}\'',
    # set an account's fields to fixture values
    "update_query": "UPDATE {schema}.order SET {set_clause} WHERE {where_clause}",
    "updates": [
        {
            # pfa / new dep / active / dates not null
            "source_criteria": {"case": "13572211"},
            "set": {
                "Ord Type": "1",
                "Ord Stat": "Active",
                "Issue Date": "2014-08-27 00:00:00",
                "Expiry Date": "2014-08-27 00:00:00",
                "Clause Expiry": "2014-08-27 00:00:00",
            },
        },
        {
            # hw / new dep / open / dates null
            "source_criteria": {"case": "95056617"},
            "set": {
                "Ord Type": "2",
                "Ord Stat": "Active",
                "Issue Date": "",
                "Expiry Date": "",
                "Clause Expiry": "",
            },
        },
        {
            # pfa / supp / closed
            "source_criteria": {"case": "11466112"},
            "set": {"Ord Type": "26", "Ord Stat": "Closed"},
        },
        {
            # pfa / replace / active
            "source_criteria": {"case": "13547686"},
            "set": {"Ord Type": "40", "Ord Stat": "Active"},
        },
        {
            # pfa / interim / open
            "source_criteria": {"case": "12779384"},
            "set": {"Ord Type": "41", "Ord Stat": "Active"},
        },
        {
            # pfa / direction / closed
            "source_criteria": {"case": "13482478"},
            "set": {"Ord Type": "43", "Ord Stat": "Closed"},
        },
        {
            # pfa / tenancy / active
            "source_criteria": {"case": "13448593"},
            "set": {"Ord Type": "45", "Ord Stat": "Active"},
        },
    ],
}
