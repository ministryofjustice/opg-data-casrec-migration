"""
Dynamic fixtures for the casrec order table for testing deputy clients
"""

DEPUTY_CLIENTS_FIXTURES = {
    "source_query": """
            SELECT "Case"
            FROM {schema}.deputy d inner join {schema}.deputyship ds ON d.\"Deputy No\" = ds.\"Deputy No\"
            WHERE "Case" = \'{case}\'
        """,
    # set an account's fields to fixture values
    "update_query": """
        UPDATE {schema}.deputy d SET {set_clause}
        FROM {schema}.deputyship ds WHERE d.\"Deputy No\" = ds.\"Deputy No\" AND {where_clause}""",
    "updates": [
        {
            # Other
            "source_criteria": {"case": "11019897"},
            "set": {"Dep Type": "5"},
        },
        {
            # Spouse
            "source_criteria": {"case": "13323382"},
            "set": {"Dep Type": "10"},
        },
        {
            # Child
            "source_criteria": {"case": "10202386"},
            "set": {"Dep Type": "11"},
        },
        {
            # Parent
            "source_criteria": {"case": "11497854"},
            "set": {"Dep Type": "12"},
        },
        {
            # Civil
            "source_criteria": {"case": "10200748"},
            "set": {"Dep Type": "13"},
        },
        {
            # Other
            "source_criteria": {"case": "10084054"},
            "set": {"Dep Type": "19"},
        },
        {
            # Bank
            "source_criteria": {"case": "10152488"},
            "set": {"Dep Type": "20"},
        },
        {
            # Solicitor
            "source_criteria": {"case": "10020983"},
            "set": {"Dep Type": "21"},
        },
        {
            # Accountant
            "source_criteria": {"case": "13567497"},
            "set": {"Dep Type": "22"},
        },
        {
            # Other
            "source_criteria": {"case": "10134672"},
            "set": {"Dep Type": "90"},
        },
        {
            # Other professional
            "source_criteria": {"case": "1346927T"},
            "set": {"Dep Type": "29"},
        },
        {
            # Friend
            "source_criteria": {"case": "10058508"},
            "set": {"Dep Type": "14"},
        },
        {
            # Partner
            "source_criteria": {"case": "94026637"},
            "set": {"Dep Type": "15"},
        },
        {
            # Panel
            "source_criteria": {"case": "1030841T"},
            "set": {"Dep Type": "63"},
        },
        {
            # Sibling
            "source_criteria": {"case": "13578754"},
            "set": {"Dep Type": "7"},
        },
        {
            # Unregulated
            "source_criteria": {"case": "10192899"},
            "set": {"Dep Type": "24"},
        },
        {
            # Legal
            "source_criteria": {"case": "13562090"},
            "set": {"Dep Type": "25"},
        },
        {
            # Middle names
            "source_criteria": {"case": "11317742"},
            "set": {"Dep Forename": "Bill Frank Amelia Spoon"},
        },
    ],
}
