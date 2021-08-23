import pandas as pd
from pandas._testing import assert_frame_equal

from utilities.standard_transformations import multiply_by_100


def test_multiply_by_100():
    new_col = "integer col"

    test_data = {
        "column_1": [0.5, 0.66, 2, 1.9],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    expected_data = {
        new_col: [50.0, 66.0, 200.0, 190.0],
    }

    expected_data_df = pd.DataFrame(expected_data, columns=[x for x in expected_data])

    result_df = multiply_by_100(
        original_col="column_1", result_col=new_col, df=test_data_df
    )

    assert_frame_equal(expected_data_df, result_df)
