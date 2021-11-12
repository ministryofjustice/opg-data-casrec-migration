import pandas as pd
from pandas._testing import assert_frame_equal

from utilities.standard_transformations import fee_reduction_end_date


def test_fee_reduction_start_date():
    new_col = "new date"

    test_data = {
        "column_1": [
            "31/03/2011 00:00",
            "01/04/2012 00:00",
            "2012-04-01 00:00:00",
            "01/05/2020 00:00",
            "04/02/2020",
        ],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    expected_data = {
        new_col: ["2011-03-31", "2012-03-31", "2012-03-31", "2021-03-31", "2020-03-31"],
    }

    expected_data_df = pd.DataFrame(expected_data, columns=[x for x in expected_data])
    expected_data_df[new_col] = pd.to_datetime(expected_data[new_col])

    result_df = fee_reduction_end_date(
        original_col="column_1", result_col=new_col, df=test_data_df
    )

    assert_frame_equal(expected_data_df, result_df)
