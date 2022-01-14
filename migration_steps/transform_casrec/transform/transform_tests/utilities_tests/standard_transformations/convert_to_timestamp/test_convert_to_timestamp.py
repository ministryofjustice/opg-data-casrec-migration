from pandas._testing import assert_frame_equal

from utilities.standard_transformations import convert_to_timestamp
import pandas as pd


def test_convert_to_timestamp():
    test_data = {
        "date_col": [
            "2020-06-12",
            "2020-06-13",
            "2020-06-14",
            "",
            "NaT",
            "2020-12-01",
        ],
        "time_col": [
            "",
            "NaT",
            "08:54:04.032000",
            "09:54:04.032000",
            "10:54:04.032000",
            "07:00:00.032000",
        ],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    expected_data = {
        "datetime_col": [
            "2020-06-11 23:00:00",
            "2020-06-12 23:00:00",
            "2020-06-14 07:54:04",
            None,
            None,
            "2020-12-01 07:00:00"
        ],
    }

    expected_data_df = pd.DataFrame(expected_data, columns=[x for x in expected_data])
    expected_data_df["datetime_col"] = pd.to_datetime(expected_data["datetime_col"], dayfirst=True, utc=True)

    result_df = convert_to_timestamp(
        original_cols=["date_col", "time_col"],
        result_col="datetime_col",
        df=test_data_df,
    )

    assert_frame_equal(expected_data_df, result_df)
