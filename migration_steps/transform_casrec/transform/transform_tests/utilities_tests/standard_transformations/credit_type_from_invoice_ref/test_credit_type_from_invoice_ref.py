import pandas as pd
from pandas._testing import assert_frame_equal

from utilities.standard_transformations import credit_type_from_invoice_ref


def test_credit_type_from_invoice_ref():
    new_col = "result col"

    test_data = {
        "column_1": [
            "somethingZ",
            "Zsomething",
            "somethingCR",
            "CRsomething",
            "somethingWO",
            "WOsomething",
        ],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    expected_data = {
        new_col: [
            "CREDIT REMISSION",
            "CREDIT REMISSION",
            "CREDIT MEMO",
            "CREDIT MEMO",
            "CREDIT WRITE OFF",
            "CREDIT WRITE OFF",
        ],
    }

    expected_data_df = pd.DataFrame(expected_data, columns=[x for x in expected_data])

    result_df = credit_type_from_invoice_ref(
        original_col="column_1", result_col=new_col, df=test_data_df
    )

    assert_frame_equal(expected_data_df, result_df)
