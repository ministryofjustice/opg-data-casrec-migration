import pandas as pd
from pandas._testing import assert_frame_equal

from transform_data.apply_conditions import greater_than


def test_greater_than():
    test_data = {
        "c_test_col": ["0.5", "0.66", "2.2", "1.9"],
    }
    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    expected_data = {
        "c_test_col": [2.2, 1.9],
    }
    expected_data_df = pd.DataFrame(expected_data, columns=[x for x in expected_data])

    test_cols = {"greater_than": {"col": "Test Col", "value": 0.66}}
    result_df = greater_than(
        df=test_data_df, cols=test_cols
    )

    assert_frame_equal(expected_data_df, result_df.reset_index(drop=True))
