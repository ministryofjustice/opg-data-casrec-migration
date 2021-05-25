from pytest_cases import case
import pandas as pd


case(id="single field has single value")


def case_single_field_single_value():
    test_data = {
        "column_1": ["row_1", "row_2", "row_3"],
        "column_2": ["elephant", "giraffe", "elephant"],
        "column_3": ["row_1", "row_2", "row_3"],
        "column_4": ["row_1", "row_2", "row_3"],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    conditions = {"column_2": "elephant"}

    result_data = {
        "column_1": ["row_1", "row_3"],
        "column_2": ["elephant", "elephant"],
        "column_3": ["row_1", "row_3"],
        "column_4": ["row_1", "row_3"],
    }

    expected_result_data_data_df = pd.DataFrame(
        result_data, columns=[x for x in result_data]
    )

    return (test_data_df, conditions, expected_result_data_data_df)


case(id="multiple field has single value")


def case_multiple_fields_single_value():
    test_data = {
        "column_1": ["row_1", "row_2", "row_3"],
        "column_2": ["elephant", "giraffe", "elephant"],
        "column_3": ["row_1", "row_2", "giraffe"],
        "column_4": ["row_1", "row_2", "row_3"],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    conditions = {"column_2": "elephant", "column_3": "giraffe"}

    result_data = {
        "column_1": ["row_3"],
        "column_2": ["elephant"],
        "column_3": ["giraffe"],
        "column_4": ["row_3"],
    }

    expected_result_data_data_df = pd.DataFrame(
        result_data, columns=[x for x in result_data]
    )

    return (test_data_df, conditions, expected_result_data_data_df)
