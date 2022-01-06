"""
Dynamic fixtures for the casrec order table for testing deputy notes
"""

DEPUTY_NOTES_FIXTURES = {
    "source_query": """
            SELECT "Case"
            FROM {schema}.deputy_remarks dr inner join {schema}.deputyship ds ON dr.\"Deputy No\" = ds.\"Deputy No\"
            WHERE "Case" = \'{case}\'
        """,
    # set an account's fields to fixture values
    "update_query": """
        UPDATE {schema}.deputy_remarks dr SET {set_clause}
        FROM {schema}.deputyship ds WHERE dr.\"Deputy No\" = ds.\"Deputy No\" AND {where_clause}""",
    "updates": [
        {
            # Internal / event_created
            "source_criteria": {"case": "10199092"},
            "set": {"Log Type": "R1"},
        },
        {
            # Incoming / event_created
            "source_criteria": {"case": "13559860"},
            "set": {"Log Type": "R8"},
        },
    ],
}
