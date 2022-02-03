"""
Dynamic fixtures for the casrec order table for testing finance credit ledger fixtures
"""
# Amount < 0 in feeexport
FINANCE_CREDIT_LEDGER_FIXTURES = {
    "source_query": 'SELECT "Case", "Invoice No" FROM {schema}.feeexport WHERE "Case" = \'{case}\' and "Invoice No" = \'{invoice_no}\'',
    # set an account's fields to fixture values
    "update_query": "UPDATE {schema}.feeexport SET {set_clause} WHERE {where_clause}",
    "updates": [
        {
            # Remission
            "source_criteria": {"case": "10072548", "invoice_no": "S300100/18"},
            "set": {
                "Invoice No": "Z300107/19",
                "Amount": "-35",
                "Orig Invoice": "S300107/19",
            },
        },
        {
            # Remission
            "source_criteria": {"case": "10090422", "invoice_no": "S200128/19"},
            "set": {
                "Invoice No": "AD48307/0Z",
                "Amount": "-17.26",
                "Orig Invoice": "AD48307/19",
            },
        },
        {
            # Memo
            "source_criteria": {"case": "10184300", "invoice_no": "AD56564/0Z"},
            "set": {
                "Invoice No": "CR56564/20",
                "Amount": "-100",
                "Orig Invoice": "AD56564/20",
            },
        },
        {
            # Memo
            "source_criteria": {"case": "10297297", "invoice_no": "AD55796/0Z"},
            "set": {
                "Invoice No": "AD55796/CR",
                "Amount": "-100",
                "Orig Invoice": "AD55796/20",
            },
        },
        {
            # Write off
            "source_criteria": {"case": "13399214", "invoice_no": "AD42677/19"},
            "set": {
                "Invoice No": "WO43687/19",
                "Amount": "-240.44",
                "Orig Invoice": "S243687/19",
            },
        },
        {
            # Write off
            "source_criteria": {"case": "13410324", "invoice_no": "AD51922/19"},
            "set": {
                "Invoice No": "S248943/WO",
                "Amount": "-11.37",
                "Orig Invoice": "S248943/19",
            },
        },
    ],
}
