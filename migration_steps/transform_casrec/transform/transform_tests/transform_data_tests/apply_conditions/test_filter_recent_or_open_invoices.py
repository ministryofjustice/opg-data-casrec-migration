import pandas as pd
from pandas._testing import assert_frame_equal

from transform_data.apply_conditions import filter_recent_or_open_invoices


def test_filter_recent_or_open_invoices():
    debt_col = "Outstanding Amount"
    test_data = {
        "c_test_date_col": [
            "10/10/2014 00:00:00",
            "31/03/2015 23:59:00",
            "01/04/2015 00:00",
            "2017-04-01 00:00:00",
        ],
        debt_col: ["100", None, None, None],
    }
    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    expected_data = {
        "c_test_date_col": [
            "10/10/2014 00:00:00",
            "01/04/2015 00:00",
            "2017-04-01 00:00:00",
        ],
        debt_col: ["100", None, None],
    }

    expected_data_df = pd.DataFrame(expected_data, columns=[x for x in expected_data])

    test_cols = {
        "recent_or_open_invoices": {"date_col": "Test Date Col", "tax_year_from": 2015}
    }
    result_df = filter_recent_or_open_invoices(
        df=test_data_df, cols=test_cols, debt_col=debt_col
    )

    assert_frame_equal(expected_data_df, result_df.reset_index(drop=True))
