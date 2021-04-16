import pandas as pd

from transform_data.calculations import do_calculations
from transform_tests.transform_data_tests.calculations import cases_calculations_called

from pytest_cases import parametrize_with_cases


test_source_data_dict = {
    "Remarks": ["row1", "row2", "row3"],
    "Logdate": ["blah", "blah", "blah"],
}

test_source_data_df = pd.DataFrame(
    test_source_data_dict, columns=[x for x in test_source_data_dict]
)


@parametrize_with_cases(
    ("test_calculation", "log_message"), cases=cases_calculations_called
)
def test_correct_calculation_called(
    caplog, mock_calculations, test_calculation, log_message
):
    do_calculations(test_calculation, test_source_data_df)

    assert log_message in caplog.text
