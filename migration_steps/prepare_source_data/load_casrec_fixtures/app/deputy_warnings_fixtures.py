"""
Dynamic fixtures for the casrec order table for testing deputy warnings
"""

DEPUTY_WARNINGS_FIXTURES = {
    "source_query": """SELECT "Case"
    FROM {schema}.deputy d
    inner join {schema}.deputyship ds ON d.\"Deputy No\" = ds.\"Deputy No\"
    WHERE "Case" = \'{case}\'""",
    # set an account's fields to fixture values
    "update_query": """
        UPDATE {schema}.deputy d SET {set_clause}
        FROM {schema}.deputyship ds WHERE d.\"Deputy No\" = ds.\"Deputy No\" AND {where_clause}""",
    "updates": [
        {
            # Violent
            "source_criteria": {"case": "10433249"},
            "set": {"VWM": "4", "SIM": "0"},
        },
        {
            # Special
            "source_criteria": {"case": "94029318"},
            "set": {"VWM": "0", "SIM": "3"},
        },
    ],
}
