import pandas as pd
from pandas.testing import assert_frame_equal

from utilities.standard_transformations import coalesce


def test_coalesce():
    test_data = {
        "id": [
            1,  # 1st source column "", 2nd None
            2,  # 1st source column None, 2nd ""
            3,  # 1st source column has value, 2nd None
            4,  # 1st source column None, 2nd has value
            5,  # both columns have a value (first should be used)
            6,  # 1st source column has a value, target column has a value and should be overridden
            7,  # 2nd source column has a value, target column has a value and should be overridden
        ],
        "Start Date": [
            "",
            None,
            "2022-02-07",
            None,
            "2022-02-09",
            "2022-02-11",
            None,
        ],
        "Actdate": [
            None,
            "",
            None,
            "2022-02-08",
            "2022-02-10",
            None,
            "2022-02-12",
        ],
        "duedate": [
            None,
            None,
            None,
            None,
            None,
            "2022-02-13",
            "2022-02-14",
        ],
    }
    test_data_df = pd.DataFrame(test_data)

    result_col = "duedate"

    expected_data = test_data.copy()
    expected_data[result_col] = [
        None,
        None,
        "2022-02-07",
        "2022-02-08",
        "2022-02-09",
        "2022-02-11",
        "2022-02-12",
    ]
    expected_data_df = pd.DataFrame(expected_data)

    result_df = coalesce(
        original_cols=[
            "Start Date",
            "Actdate",
        ],
        result_col=result_col,
        df=test_data_df,
    )

    assert_frame_equal(expected_data_df, result_df)
