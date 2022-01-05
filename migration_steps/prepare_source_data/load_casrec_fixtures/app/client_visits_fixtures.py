"""
Dynamic fixtures for the casrec order table for testing client visits
"""

CLIENT_VISITS_FIXTURES = {
    "source_query": 'SELECT "Case" FROM {schema}.repvis WHERE "Case" = \'{case}\'',
    "update_query": "UPDATE {schema}.repvis SET {set_clause} WHERE {where_clause}",
    "updates": [
        {
            #
            "source_criteria": {"case": "10486336"},
            "set": {"Req By": "1", "Outcome": "0", "Reason": "4", "Categ": "Green"},
        },
        {
            #
            "source_criteria": {"case": "11203189"},
            "set": {"Req By": "2", "Outcome": "1", "Reason": "1", "Categ": "Amber"},
        },
        {
            #
            "source_criteria": {"case": "11084211"},
            "set": {"Req By": "3", "Outcome": "2", "Reason": "1", "Categ": "Blue"},
        },
        {
            #
            "source_criteria": {"case": "13611831"},
            "set": {"Req By": "4", "Outcome": "3", "Reason": "1", "Categ": "Red"},
        },
        {
            #
            "source_criteria": {"case": "13263316"},
            "set": {"Req By": "5", "Outcome": "4", "Reason": "5", "Categ": "Green"},
        },
        {
            #
            "source_criteria": {"case": "10297913"},
            "set": {"Req By": "6", "Outcome": "5", "Reason": "6", "Categ": "Green"},
        },
        {
            #
            "source_criteria": {"case": "10114095"},
            "set": {"Req By": "7", "Outcome": "6", "Reason": "3", "Categ": "Green"},
        },
        {
            #
            "source_criteria": {"case": "12882401"},
            "set": {"Req By": "8", "Outcome": "7", "Reason": "7", "Categ": "Green"},
        },
        {
            #
            "source_criteria": {"case": "10445671"},
            "set": {"Req By": "9", "Outcome": "8", "Reason": "8", "Categ": "Green"},
        },
        {
            #
            "source_criteria": {"case": "10082290"},
            "set": {"Req By": "10", "Outcome": "9", "Reason": "2", "Categ": "Green"},
        },
        {
            #
            "source_criteria": {"case": "13527247"},
            "set": {"Req By": "11", "Outcome": "10", "Reason": "9", "Categ": "Green"},
        },
        {
            #
            "source_criteria": {"case": "12217002"},
            "set": {"Req By": "12", "Outcome": "11", "Reason": "10", "Categ": "Green"},
        },
        {
            #
            "source_criteria": {"case": "10243443"},
            "set": {"Req By": "13", "Outcome": "11", "Reason": "11", "Categ": "Green"},
        },
        {
            #
            "source_criteria": {"case": "1294953T"},
            "set": {"Req By": "14", "Outcome": "11", "Reason": "0", "Categ": "Green"},
        },
    ],
}
