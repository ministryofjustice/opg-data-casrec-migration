import pandas as pd
from pandas.testing import assert_frame_equal

from utilities.standard_transformations import is_at_least_one_set


def test_is_at_least_one_set():
    test_data = {
        "id": [1, 2, 3],
        "received_date1": [
            "2021-01-01",
            None,
            "",
        ],
        "received_date2": [
            "2021-02-02",
            None,
            None,
        ],
        "received_date3": [
            "2021-03-03",
            None,
            None,
        ],
        "received_date4": [
            None,
            None,
            "",
        ]
    }
    test_data_df = pd.DataFrame(test_data)

    result_col = "has_received_date"

    expected_data = test_data.copy()
    expected_data[result_col] = [True, False, False]
    expected_data_df = pd.DataFrame(expected_data)

    result_df = is_at_least_one_set(
        original_cols=["received_date1", "received_date2", "received_date3", "received_date4"],
        result_col=result_col,
        df=test_data_df
    )

    assert_frame_equal(expected_data_df, result_df)
