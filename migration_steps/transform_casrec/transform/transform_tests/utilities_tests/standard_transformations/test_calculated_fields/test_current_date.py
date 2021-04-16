from datetime import datetime

import pandas as pd


from utilities.standard_calculations import current_date


def test_current_date():

    test_data = {
        "column_1": [str(x) for x in range(0, 10)],
        "column_2": [str(x * x) for x in range(0, 10)],
        "column_3": [str(x * x * x) for x in range(0, 10)],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    result_df = current_date(column_name="todays_date", df=test_data_df)

    assert "todays_date" in result_df.columns.values.tolist()
    assert result_df.sample()["todays_date"].values == datetime.today().strftime(
        "%Y-%m-%d"
    )
