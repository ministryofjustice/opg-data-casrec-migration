"""
Dynamic fixtures for the casrec order table for testing client notes
"""

CLIENT_NOTES_FIXTURES = {
    "source_query": 'SELECT "Case" FROM {schema}.remarks WHERE "Case" = \'{case}\'',
    # set an account's fields to fixture values
    "update_query": "UPDATE {schema}.remarks SET {set_clause} WHERE {where_clause}",
    # casrec accounts with the dates set below will be transformed to
    # Sirius annual_report_log records with the status and reviewstatus shown
    "updates": [
        {
            # Internal / event_created
            "source_criteria": {"case": "1005934T"},
            "set": {"Log Type": "R1"},
        },
        {
            # Incoming / event_created
            "source_criteria": {"case": "13612644"},
            "set": {"Log Type": "R8"},
        },
    ],
}
