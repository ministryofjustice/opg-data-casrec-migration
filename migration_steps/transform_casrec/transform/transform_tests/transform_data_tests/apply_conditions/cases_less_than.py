from pytest_cases import case
import pandas as pd


case(id="bring back records less than float number")


def case_less_than():
    test_data = {
        "c_test_col": ["0.5", "0.66", "2.2", "1.9"],
    }
    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    conditions = {"less_than": {"col": "Test Col", "value": 0.66}}

    expected_data = {
        "c_test_col": [0.5],
    }
    expected_result_data_data_df = pd.DataFrame(
        expected_data, columns=[x for x in expected_data]
    )

    return (test_data_df, conditions, expected_result_data_data_df)
