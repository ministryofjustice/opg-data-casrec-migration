"""
Dynamic fixtures for the casrec order table
"""

ORDER_FIXTURES = [
    {
        "source_query": 'SELECT "Order No" FROM {schema}.order WHERE "Case" = \'{case}\' AND "Ord Type" = \'{order_type}\'',
        "update_query": "UPDATE {schema}.order SET {set_clause} WHERE {where_clause}",
        "updates": [
            {
                "source_criteria": {
                    "case": "95050777",
                    "order_type": "26"
                },
                "set": {
                    "Ord Stat": "Active"
                },
            },
            {
                "source_criteria": {
                    "case": "95049684",
                    "order_type": "26"
                },
                "set": {
                    "Ord Stat": "Active",
                    "Ord Type": "43"
                },
            },
            {
                "source_criteria": {
                    "case": "95014298",
                    "order_type": "26"
                },
                "set": {
                    "Ord Stat": "Active",
                    "Ord Type": "45"
                },
            }
        ],
    }
]
