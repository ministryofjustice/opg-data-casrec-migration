from pytest_cases import case
import pandas as pd

case(id="find latest grouped by two ids")


def case_latest():
    test_data = {
        "c_column_id": ["1", "1", "2", "2"],
        "c_column_date_time": [
            "2021-01-01 00:00:00",
            "2020-06-01 00:00:00",
            "2060-01-01 00:00:00",
            "2020-09-01 00:00:00",
        ],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    conditions = {"latest": {"col": "column_date_time", "per": "column_id"}}

    result_data = {
        "c_column_id": ["1", "2"],
        "c_column_date_time": ["2021-01-01 00:00:00", "2060-01-01 00:00:00"],
    }

    expected_result_data_data_df = pd.DataFrame(
        result_data, columns=[x for x in result_data]
    )

    return (test_data_df, conditions, expected_result_data_data_df)
