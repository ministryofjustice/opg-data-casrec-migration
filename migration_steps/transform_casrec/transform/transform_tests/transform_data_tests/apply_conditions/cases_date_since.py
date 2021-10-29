from pytest_cases import case
import pandas as pd


case(id="bring back records where date is on or after X")


def case_date_since():
    test_data = {
        "c_test_col": [
            "01/04/2014 00:00:00",
            "01/04/2014",
            "2014-04-01",
            "31/03/2014",
            "10/10/2014",
        ],
    }
    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    conditions = {"date_since": {"col": "Test Col", "date": "01/04/2014"}}

    expected_data = {
        "c_test_col": [
            "01/04/2014 00:00:00",
            "01/04/2014",
            "2014-04-01",
            "10/10/2014",
        ],
    }
    expected_result_data_data_df = pd.DataFrame(
        expected_data, columns=[x for x in expected_data]
    )

    return (test_data_df, conditions, expected_result_data_data_df)
