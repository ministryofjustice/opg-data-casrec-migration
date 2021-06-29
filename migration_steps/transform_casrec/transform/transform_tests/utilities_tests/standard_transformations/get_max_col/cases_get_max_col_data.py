import json

from pytest_cases import case
import pandas as pd


@case(id="get max value - value is an int")
def case_get_max_int():
    test_data = {
        "column_1": 1,
        "column_2": 2,
        "column_3": 3,
        "column_4": None,
        "column_5": None,
        "column_6": None,
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data], index=[0])
    test_cols = test_data_df.columns.tolist()
    test_result_col = "final_col"

    expected_result = {"final_col": 3}

    expected_result_df = pd.DataFrame(
        expected_result, columns=[x for x in expected_result], index=[0]
    )

    return (test_data_df, test_cols, test_result_col, expected_result_df)
