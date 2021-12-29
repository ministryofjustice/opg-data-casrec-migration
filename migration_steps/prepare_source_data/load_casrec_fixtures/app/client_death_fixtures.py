"""
Dynamic fixtures for the casrec order table for testing bonds
"""

BOND_FIXTURES = {
    "source_query": 'SELECT "Case" FROM {schema}.pat WHERE "Case" = \'{case}\'',
    # set an account's fields to fixture values
    "update_query": "UPDATE {schema}.order SET {set_clause} WHERE {where_clause}",
    # casrec accounts with the dates set below will be transformed to
    # Sirius annual_report_log records with the status and reviewstatus shown
    "updates": [
        {
            # Fax
            "source_criteria": {"case": "10207131"},
            "set": {"Notify": "4"},
        },
        {
            # Letter
            "source_criteria": {"case": "13560544"},
            "set": {"Bond Co": "3"},
        },
        {
            # Email
            "source_criteria": {"case": "10243489"},
            "set": {"Bond Co": "2"},
        },
        {
            # Phone
            "source_criteria": {"case": "13539594"},
            "set": {"Bond Co": "1"},
        },
    ],
}
