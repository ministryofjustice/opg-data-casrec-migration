from decimal import Decimal

import pandas as pd
from pandas._testing import assert_frame_equal

from utilities.standard_transformations import absolute_value


def test_absolute_value():
    new_col = "result col"

    test_data = {
        "column_1": ["-0.5", "0.66", "-2", "1.9"],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    expected_data = {
        new_col: [Decimal("0.5"), Decimal("0.66"), Decimal("2"), Decimal("1.9")],
    }

    expected_data_df = pd.DataFrame(expected_data, columns=[x for x in expected_data])

    result_df = absolute_value(
        original_col="column_1", result_col=new_col, df=test_data_df
    )

    assert_frame_equal(expected_data_df, result_df)
