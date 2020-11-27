from tests.utilities.standard_transformations.convert_to_bool import (
    cases_convert_to_bool_shape,
    cases_convert_to_bool_data,
)

from utilities.standard_transformations import convert_to_bool
from pytest_cases import parametrize_with_cases
import pandas as pd


@parametrize_with_cases(
    (
        "test_data_df",
        "original_col",
        "new_col",
        "drop_original_col",
        "result_column_list",
    ),
    cases=cases_convert_to_bool_shape,
)
def test_convert_to_bool_shape(
    test_data_df, original_col, new_col, drop_original_col, result_column_list
):
    result_df = convert_to_bool(original_col, new_col, test_data_df, drop_original_col)

    assert result_df.columns.values.tolist() == result_column_list


@parametrize_with_cases(
    ("test_data_df", "original_col", "new_col", "expected_result",),
    cases=cases_convert_to_bool_data,
)
def test_convert_to_bool_data(test_data_df, original_col, new_col, expected_result):
    result_df = convert_to_bool(original_col, new_col, test_data_df)

    print(expected_result.to_markdown())
    print(result_df.to_markdown())

    pd.testing.assert_frame_equal(result_df, expected_result)
