import re

from pytest_cases import parametrize_with_cases

from tests.transformations.transformations_from_mapping.cases import (
    cases_generate_select_statement_2,
)
from transformations.generate_source_query_new import (
    generate_select_string_from_mapping,
)


@parametrize_with_cases(
    ("mapping", "source_table_name", "additional_columns", "expected_result"),
    cases=cases_generate_select_statement_2,
)
def test_generate_select_string_from_mapping(
    mapping, source_table_name, additional_columns, expected_result
):
    result = generate_select_string_from_mapping(
        mapping=mapping,
        source_table_name=source_table_name,
        additional_columns=additional_columns,
        db_schema="etl1",
    )

    assert sorted(result.split()) == sorted(expected_result.split())
