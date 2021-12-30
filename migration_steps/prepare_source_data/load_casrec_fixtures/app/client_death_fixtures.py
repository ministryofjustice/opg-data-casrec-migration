"""
Dynamic fixtures for the casrec order table for testing bonds
"""

CLIENT_DEATH_FIXTURES = {
    "source_query": 'SELECT "Case" FROM {schema}.pat WHERE "Case" = \'{case}\'',
    # set an account's fields to fixture values
    "update_query": "UPDATE {schema}.pat SET {set_clause} WHERE {where_clause}",
    # casrec accounts with the dates set below will be transformed to
    # Sirius annual_report_log records with the status and reviewstatus shown
    "updates": [
        {
            # Fax
            "source_criteria": {"case": "13045198"},
            "set": {
                "Notify": "4",
                "Proof": "Y",
                "Term by": "D",
                "Notified": "2019-03-02 00:00:00",
                "Letter Sent": "2019-03-02 00:00:00",
            },
        },
        {
            # Letter
            "source_criteria": {"case": "11013596"},
            "set": {
                "Notify": "3",
                "Proof": "Y",
                "Term by": "E",
                "Notified": "2020-03-02 00:00:00",
                "Letter Sent": "2020-03-02 00:00:00",
            },
        },
        {
            # Email
            "source_criteria": {"case": "11553037"},
            "set": {
                "Notify": "2",
                "Proof": "Y",
                "Term by": "O",
                "Notified": "2021-03-02 00:00:00",
                "Letter Sent": "2021-03-02 00:00:00",
            },
        },
        {
            # Phone
            "source_criteria": {"case": "11565044"},
            "set": {
                "Notify": "1",
                "Proof": "N",
                "Term by": "O",
                "Notified": "2019-03-02 00:00:00",
                "Letter Sent": "",
            },
        },
    ],
}
