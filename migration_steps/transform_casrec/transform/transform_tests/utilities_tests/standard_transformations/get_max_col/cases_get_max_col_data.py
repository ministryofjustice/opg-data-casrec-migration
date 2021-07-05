import json

from pytest_cases import case
import pandas as pd
import numpy as np


class MaxValueCases:
    @case(id="get max value - value is an int")
    def case_get_max_int(self):
        test_data = {
            "column_1": [1, 1, 6, 1, 1],
            "column_2": [2, 1, 5, 0, 2],
            "column_3": [3, 1, 4, None, 3],
            "column_4": [4, 1, 3, 0, None],
            "column_5": [5, 1, 2, 1, None],
            "column_6": [6, 1, 1, 0, None],
        }

        test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])
        test_cols = test_data_df.columns.tolist()
        test_result_col = "final_col"

        expected_result = {"final_col": [6.0, 1.0, 6.0, 1.0, 3.0]}

        expected_result_df = pd.DataFrame(
            expected_result, columns=[x for x in expected_result]
        )

        return (test_data_df, test_cols, test_result_col, expected_result_df)

    @case(id="get max value - value is a mixture of float and ints")
    def case_get_max_int_and_float(self):
        test_data = {
            "column_1": [1.1, 1],
            "column_2": [2.1, 2],
            "column_3": [3.1, 3.6],
            "column_4": [4.1, 9.8],
            "column_5": [5.1, 10],
            "column_6": [6.1, 0.3],
        }

        test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])
        test_cols = test_data_df.columns.tolist()
        test_result_col = "final_col"

        expected_result = {"final_col": [6.1, 10.0]}

        expected_result_df = pd.DataFrame(
            expected_result, columns=[x for x in expected_result]
        )

        return (test_data_df, test_cols, test_result_col, expected_result_df)

    @case(id="get max value - value is a date")
    def case_get_max_date(self):
        test_data = {
            "column_1": "2015-01-01",
            "column_2": "2016-01-01",
            "column_3": "2017-01-01",
            "column_4": "",
            "column_5": "",
            "column_6": "",
        }

        test_data_df = pd.DataFrame(
            test_data, columns=[x for x in test_data], index=[0]
        )
        test_cols = test_data_df.columns.tolist()
        test_result_col = "final_col"

        expected_result = {"final_col": "2017-01-01"}

        expected_result_df = pd.DataFrame(
            expected_result, columns=[x for x in expected_result], index=[0]
        )

        return (test_data_df, test_cols, test_result_col, expected_result_df)
