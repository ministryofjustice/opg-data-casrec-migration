from transform_tests.utilities.standard_transformations.squash_columns import (
    cases_squash_columns_shape,
    cases_squash_columns_data,
)
from utilities.standard_transformations import squash_columns
from pytest_cases import parametrize_with_cases
import pandas as pd


@parametrize_with_cases(
    (
        "test_data_df",
        "cols_to_squash",
        "new_col",
        "drop_original_cols",
        "result_column_list",
    ),
    cases=cases_squash_columns_shape,
)
def test_squash_columns_shape(
    test_data_df, cols_to_squash, new_col, drop_original_cols, result_column_list
):
    result_df = squash_columns(
        cols_to_squash, new_col, test_data_df, drop_original_cols
    )

    assert result_df.columns.values.tolist() == result_column_list


@parametrize_with_cases(
    ("test_data_df", "cols_to_squash", "new_col", "expected_result",),
    cases=cases_squash_columns_data,
)
def test_squash_columns_data(test_data_df, cols_to_squash, new_col, expected_result):
    result_df = squash_columns(cols_to_squash, new_col, test_data_df)

    print(expected_result.to_markdown())
    print(result_df.to_markdown())

    pd.testing.assert_frame_equal(result_df, expected_result)
