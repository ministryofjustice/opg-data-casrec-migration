"""
Dynamic fixtures for the casrec order table for testing client warnings
"""

CLIENT_WARNINGS_FIXTURES = {
    "source_query": 'SELECT "Case" FROM {schema}.pat WHERE "Case" = \'{case}\'',
    # set an account's fields to fixture values
    "update_query": "UPDATE {schema}.pat SET {set_clause} WHERE {where_clause}",
    "updates": [
        {
            # Violent
            "source_criteria": {"case": "10000884"},
            "set": {"VWM": "4", "SIM": "0", "SAAR Check": "N", "Debt chase": "0"},
        },
        {
            # Special
            "source_criteria": {"case": "10001403"},
            "set": {"VWM": "0", "SIM": "3", "SAAR Check": "N", "Debt chase": "0"},
        },
        {
            # Saar
            "source_criteria": {"case": "10001668"},
            "set": {"VWM": "0", "SIM": "0", "SAAR Check": "Y", "Debt chase": "0"},
        },
        {
            # Debt
            "source_criteria": {"case": "10002199"},
            "set": {"VWM": "0", "SIM": "0", "SAAR Check": "N", "Debt chase": "1"},
        },
    ],
}
