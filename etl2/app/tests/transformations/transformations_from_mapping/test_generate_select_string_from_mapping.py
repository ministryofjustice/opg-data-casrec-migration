import re

from transformations.generate_source_query import generate_select_string_from_mapping

mapping = {
    "simple_mapping": {
        "orderdate": {
            "casrec_table": "ORDER",
            "casrec_column_name": "Made Date",
            "alias": "Made Date",
        },
        "orderissuedate": {
            "casrec_table": "ORDER",
            "casrec_column_name": "Issue Date",
            "alias": "Issue Date",
        },
        "orderexpirydate": {
            "casrec_table": "ORDER",
            "casrec_column_name": "Made Date",
            "alias": "Made Date 1",
        },
        "statusdate": {
            "casrec_table": "ORDER",
            "casrec_column_name": "Made Date",
            "alias": "Made Date 2",
        },
        "caserecnumber": {
            "casrec_table": "ORDER",
            "casrec_column_name": "Case",
            "alias": "Case",
        },
        "ordersubtype": {
            "casrec_table": "ORDER",
            "casrec_column_name": "Ord Type",
            "alias": "Ord Type",
        },
        "casrec_id": {
            "casrec_table": "order",
            "casrec_column_name": "rct",
            "alias": "rct",
        },
    },
    "transformations": {
        "unique_number": [{"original_columns": ["unknown"], "aggregate_col": "uid"}]
    },
    "required_columns": {"type": {"data_type": "str", "default_value": "order"}},
}

source_table_name = "order"
additional_columns = ["Order No"]


expected_result = """
    SELECT
        "Made Date" as "Made Date",
        "Issue Date" as "Issue Date",
        "Made Date" as "Made Date 1",
        "Made Date" as "Made Date 2",
        "Case" as "Case",
        "Ord Type" as "Ord Type",
        "rct" as "rct",
        "Order No" as "c_order_no"
    FROM etl1.order;
"""


def test_generate_select_string_from_mapping():
    result = generate_select_string_from_mapping(
        mapping, source_table_name, additional_columns, db_schema="etl1"
    )

    assert result.split() == expected_result.split()
