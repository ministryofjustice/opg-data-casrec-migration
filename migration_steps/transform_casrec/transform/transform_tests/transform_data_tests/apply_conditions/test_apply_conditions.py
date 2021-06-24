import pandas as pd

from pytest_cases import parametrize_with_cases

from transform_data.apply_conditions import source_conditions
from transform_tests.transform_data_tests.apply_conditions import (
    cases_not_null_condition,
    cases_condition_with_value,
)

from transform_data_tests.apply_conditions.cases_convert_to_timestamp import (
    case_convert_to_timestamp,
)


@parametrize_with_cases(
    ("test_data_df", "conditions", "expected_result_data_data_df"),
    cases=[
        cases_not_null_condition,
        cases_condition_with_value,
        case_convert_to_timestamp,
    ],
)
def test_apply_conditions(test_data_df, conditions, expected_result_data_data_df):

    result_df = source_conditions(df=test_data_df, conditions=conditions)

    pd.testing.assert_frame_equal(result_df, expected_result_data_data_df)
