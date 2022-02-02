"""
Dynamic fixtures for the casrec order table for testing finance credit ledger fixtures
"""

FINANCE_CREDIT_LEDGER_FIXTURES = {
    "source_query": 'SELECT "Case" FROM {schema}.feeexport WHERE "Case" = \'{case}\'',
    # set an account's fields to fixture values
    "update_query": "UPDATE {schema}.feeexport SET {set_clause} WHERE {where_clause}",
    "updates": [
        {
            # Blah
            "source_criteria": {"case": "10000884"},
            "set": {"Invoice No": "4"},
        },
    ],
}
