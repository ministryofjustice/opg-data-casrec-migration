import pandas as pd
from pandas._testing import assert_frame_equal

from utilities.standard_transformations import first_two_chars


def test_first_two_chars():
    new_col = "two chars"

    test_data = {
        "column_1": ["123456", "mBnasdg", "a", "kk", ""],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    expected_data = {
        new_col: ["12", "mB", "a", "kk", ""],
    }

    expected_data_df = pd.DataFrame(expected_data, columns=[x for x in expected_data])

    result_df = first_two_chars(
        original_col="column_1", result_col=new_col, df=test_data_df
    )

    assert_frame_equal(expected_data_df, result_df)
