"""
Dynamic fixtures for the casrec order and pat tables for testing client visits
"""
# ** As duplicates don't get mapped currently, we have replaced with closed statuses though
# if we decide to add them then they will be handled as per app logic.

CLIENT_STATUS_FIXTURES_ORDER = {
    "source_query": 'SELECT "CoP Case", "Case" FROM {schema}.order WHERE "CoP Case" = \'{cop_case}\'',
    "update_query": "UPDATE {schema}.order SET {set_clause} WHERE {where_clause}",
    "updates": [
        # Dead notified (adding some other dates anyway) - DEATH_NOTIFIED
        {
            "source_criteria": {"cop_case": "1000592801"},
            "set": {"Made Date": "2000-08-23", "Ord Stat": "Closed", "Ord Type": "26"},
        },
        {
            "source_criteria": {"cop_case": "1000592802"},
            "set": {"Made Date": "2001-08-23", "Ord Stat": "Closed", "Ord Type": "1"},
        },
        # Dead proof (adding some other dates anyway) - DEATH_CONFIRMED
        {
            "source_criteria": {"cop_case": "1000631501"},
            "set": {"Made Date": "2000-08-23", "Ord Stat": "Closed", "Ord Type": "1"},
        },
        {
            "source_criteria": {"cop_case": "1000631502"},
            "set": {"Made Date": "2001-08-23", "Ord Stat": "Active", "Ord Type": "1"},
        },
        # Latest order Active - ACTIVE
        {
            "source_criteria": {"cop_case": "1001623501"},
            "set": {"Made Date": "2000-08-23", "Ord Stat": "Closed", "Ord Type": "1"},
        },
        {
            "source_criteria": {"cop_case": "1001623502"},
            "set": {"Made Date": "2001-08-23", "Ord Stat": "Active", "Ord Type": "1"},
        },
        # Previous order Active - ACTIVE
        {
            "source_criteria": {"cop_case": "1001643101"},
            "set": {"Made Date": "2000-08-23", "Ord Stat": "Active", "Ord Type": "1"},
        },
        {
            "source_criteria": {"cop_case": "1001643102"},
            "set": {"Made Date": "2001-08-23", "Ord Stat": "Closed", "Ord Type": "1"},
        },
        # Duplicate and closed orders latest subtype 40 - CLOSED **
        {
            "source_criteria": {"cop_case": "1001666701"},
            "set": {"Made Date": "2001-08-23", "Ord Stat": "Closed", "Ord Type": "40"},
        },
        {
            "source_criteria": {"cop_case": "1001666702"},
            "set": {"Made Date": "2002-08-23", "Ord Stat": "Closed", "Ord Type": "40"},
        },
        # Duplicate and closed orders latest subtype 5 - INACTIVE **
        {
            "source_criteria": {"cop_case": "1001718101"},
            "set": {"Made Date": "2000-08-01", "Ord Stat": "Closed", "Ord Type": "5"},
        },
        {
            "source_criteria": {"cop_case": "1001718102"},
            "set": {"Made Date": "2001-08-01", "Ord Stat": "Closed", "Ord Type": "5"},
        },
        # Latest status Open - OPEN
        {
            "source_criteria": {"cop_case": "1001937701"},
            "set": {"Made Date": "2010-08-23", "Ord Stat": "Closed", "Ord Type": "26"},
        },
        {
            "source_criteria": {"cop_case": "1001937702"},
            "set": {"Made Date": "2011-08-23", "Ord Stat": "Active", "Ord Type": "26"},
        },
        # All duplicate subtype 5 - DUPLICATE **
        # {
        #     "source_criteria": {"cop_case": "1002065T01"},
        #     "set": {"Made Date": "2010-08-23", "Ord Stat": "Duplicate", "Ord Type": "5"},
        # },
        # {
        #     "source_criteria": {"cop_case": "1002065T02"},
        #     "set": {"Made Date": "2011-08-23", "Ord Stat": "Duplicate", "Ord Type": "5"},
        # },
    ],
}

CLIENT_STATUS_FIXTURES_DEATH = {
    "source_query": 'SELECT "Case" FROM {schema}.pat WHERE "Case" = \'{case}\'',
    "update_query": "UPDATE {schema}.pat SET {set_clause} WHERE {where_clause}",
    "updates": [
        # Dead notified but no proof
        {
            "source_criteria": {"case": "10005928"},
            "set": {"Notified": "2015-08-17", "Proof": "N", "Term Type": "D"},
        },
        # Dead notified with proof
        {
            "source_criteria": {"case": "10006315"},
            "set": {"Notified": "2015-08-19", "Proof": "Y", "Term Type": "D"},
        },
        # Latest order Active - ACTIVE
        {
            "source_criteria": {"case": "10016235"},
            "set": {"Notified": "2015-08-19", "Proof": "", "Term Type": ""},
        },
        # Previous order Active - ACTIVE
        {
            "source_criteria": {"case": "10016431"},
            "set": {"Notified": "", "Proof": "", "Term Type": ""},
        },
        # Duplicate and closed orders latest subtype 40 - CLOSED
        {
            "source_criteria": {"case": "10016667"},
            "set": {"Notified": "", "Proof": "", "Term Type": ""},
        },
        # Duplicate and closed orders latest subtype 5 - INACTIVE
        {
            "source_criteria": {"case": "10017181"},
            "set": {"Notified": "", "Proof": "", "Term Type": ""},
        },
        # Latest status Open - OPEN
        {
            "source_criteria": {"case": "10019377"},
            "set": {"Notified": "", "Proof": "", "Term Type": ""},
        },
        # All duplicate subtype 5 - DUPLICATE
        # {
        #     "source_criteria": {"case": "1002065T"},
        #     "set": {"Notified": "", "Proof": "", "Term Type": ""},
        # },
    ],
}
