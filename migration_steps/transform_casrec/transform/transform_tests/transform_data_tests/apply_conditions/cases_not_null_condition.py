from pytest_cases import case
import pandas as pd


case(id="single field cannot be null")


def case_single_not_null():
    test_data = {
        "column_1": ["row_1", "row_2", "row_3"],
        "column_2": ["row_1", "", "row_3"],
        "column_3": ["row_1", "row_2", "row_3"],
        "column_4": ["row_1", "row_2", "row_3"],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    conditions = {"column_2": "not null"}

    result_data = {
        "column_1": ["row_1", "row_3"],
        "column_2": ["row_1", "row_3"],
        "column_3": ["row_1", "row_3"],
        "column_4": ["row_1", "row_3"],
    }

    expected_result_data_data_df = pd.DataFrame(
        result_data, columns=[x for x in result_data]
    )

    return (test_data_df, conditions, expected_result_data_data_df)


case(id="multiple fields cannot be null")


def case_multiple_not_null():
    test_data = {
        "column_1": ["row_1", "row_2", "row_3"],
        "column_2": ["row_1", "", ""],
        "column_3": ["", "", "row_3"],
        "column_4": ["row_1", "row_2", "row_3"],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    conditions = {"column_2": "not null", "column_3": "not null"}

    result_data = {
        "column_1": ["row_1", "row_3"],
        "column_2": ["row_1", ""],
        "column_3": ["", "row_3"],
        "column_4": ["row_1", "row_3"],
    }

    expected_result_data_data_df = pd.DataFrame(
        result_data, columns=[x for x in result_data]
    )

    return (test_data_df, conditions, expected_result_data_data_df)
