import pandas as pd

from tests.transform_data.simple_transformations import cases_transformations_called

from pytest_cases import parametrize_with_cases

from transform_data.simple_transformations import do_simple_transformations

test_source_data_dict = {
    "Remarks": ["row1", "row2", "row3"],
    "Logdate": ["blah", "blah", "blah"],
}

test_source_data_df = pd.DataFrame(
    test_source_data_dict, columns=[x for x in test_source_data_dict]
)


@parametrize_with_cases(
    ("test_transformation", "log_message"), cases=cases_transformations_called
)
def test_correct_transformation_called(
    caplog, mock_standard_transformations, test_transformation, log_message
):
    do_simple_transformations(test_transformation, test_source_data_df)

    assert log_message in caplog.text
