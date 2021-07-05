from utilities.standard_transformations import get_max_col


from pytest_cases import parametrize_with_cases
import pandas as pd


from transform_tests.utilities_tests.standard_transformations.get_max_col.cases_get_max_col_data import (
    MaxValueCases,
)


@parametrize_with_cases(
    ("test_data_df", "test_cols", "test_result_col", "expected_result_df"),
    cases=MaxValueCases,
)
def test_get_max_cols(test_data_df, test_cols, test_result_col, expected_result_df):

    result_df = get_max_col(
        original_cols=test_cols, result_col=test_result_col, df=test_data_df
    )

    print("result")
    print(result_df)
    print(result_df.info())

    print("expected")
    print(expected_result_df)
    print(expected_result_df.info())

    pd.testing.assert_frame_equal(result_df, expected_result_df)
