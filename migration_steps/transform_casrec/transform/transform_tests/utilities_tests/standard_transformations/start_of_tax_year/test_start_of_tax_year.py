import pandas as pd
from pandas._testing import assert_frame_equal

from utilities.standard_transformations import start_of_tax_year


def test_start_of_tax_year():
    new_col = "start of tax year"

    test_data = {
        "column_1": [
            "28/02/2011 00:00",
            "29/06/2012 00:00",
            "2012-03-31 00:00:00",
            "01/04/2012 00:00",
        ],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    expected_data = {
        new_col: ["2010-04-01", "2012-04-01", "2011-04-01", "2012-04-01"],
    }

    expected_data_df = pd.DataFrame(expected_data, columns=[x for x in expected_data])
    expected_data_df[new_col] = pd.to_datetime(expected_data[new_col], dayfirst=True)

    result_df = start_of_tax_year(
        original_col="column_1", result_col=new_col, df=test_data_df
    )

    assert_frame_equal(expected_data_df, result_df)
