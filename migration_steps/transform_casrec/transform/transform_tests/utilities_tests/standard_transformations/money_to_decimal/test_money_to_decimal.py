from decimal import Decimal

import pandas as pd
from pandas._testing import assert_frame_equal

from utilities.standard_transformations import money_to_decimal


def test_money_to_decimal():
    new_col = "result col"

    test_data = {
        "column_1": ["0.5", "0.66", "20", "1.9", "0.57"],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    expected_data = {
        new_col: [Decimal("0.5"), Decimal("0.66"), Decimal("20"), Decimal("1.9"), Decimal("0.57")],
    }

    expected_data_df = pd.DataFrame(expected_data, columns=[x for x in expected_data])

    result_df = money_to_decimal(
        original_col="column_1", result_col=new_col, df=test_data_df
    )

    assert_frame_equal(expected_data_df, result_df)
