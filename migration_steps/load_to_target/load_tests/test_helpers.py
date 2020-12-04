from pytest_cases import parametrize_with_cases

from load_tests.test_cases import cases_get_cols_from_mapping
from load_to_target_helpers import get_cols_from_mapping


@parametrize_with_cases(
    ("include_columns", "exclude_columns", "reorder_cols", "expected_result"),
    cases=cases_get_cols_from_mapping,
)
def test_get_cols_from_mapping(
    mock_get_mapping_dict,
    include_columns,
    exclude_columns,
    reorder_cols,
    expected_result,
):

    result = get_cols_from_mapping(
        file_name="fake_file",
        include_columns=include_columns,
        exclude_columns=exclude_columns,
        reorder_cols=reorder_cols,
    )

    assert result == expected_result
