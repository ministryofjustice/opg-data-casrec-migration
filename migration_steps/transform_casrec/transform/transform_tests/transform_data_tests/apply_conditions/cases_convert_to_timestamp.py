from pytest_cases import case
import pandas as pd


case(id="convert two fields to timestamp")


def case_convert_to_timestamp():
    test_data = {
        "column_1": ["2020-06-12", "2020-06-13", "2020-06-14"],
        "column_2": ["08:54:04.032000", "09:54:04.032000", "10:54:04.032000"],
        "column_3": ["row_2", "row_2", "row_3"],
        "column_4": ["row_1", "row_2", "row_3"],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    conditions = {
        "convert_to_timestamp": {"date": "column_1", "time": "column_2"},
        "latest": {"col": "timestamp", "per": "column_3"},
    }

    result_data = {
        "column_1": ["2020-06-13", "2020-06-14"],
        "column_2": ["09:54:04.032000", "10:54:04.032000"],
        "column_3": ["row_2", "row_3"],
        "column_4": ["row_2", "row_3"],
        "timestamp": ["2020-06-13 09:54:04", "2020-06-14 10:54:04"],
    }

    # result_data = {
    #     "column_1": ["2020-06-12", "2020-06-13", "2020-06-14"],
    #     "column_2": ["08:54:04.032000", "09:54:04.032000", "10:54:04.032000"],
    #     "column_3": ["row_1", "row_2", "row_3"],
    #     "column_4": ["row_1", "row_2", "row_3"],
    #     "timestamp": ["2020-06-12 08:54:04", "2020-06-13 09:54:04", "2020-06-14 10:54:04"],
    # }

    expected_result_data_data_df = pd.DataFrame(
        result_data, columns=[x for x in result_data]
    )

    expected_result_data_data_df = expected_result_data_data_df.astype(
        {"timestamp": "datetime64[ns]"}
    )

    return (test_data_df, conditions, expected_result_data_data_df)
