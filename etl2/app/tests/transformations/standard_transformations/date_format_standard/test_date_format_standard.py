import pandas as pd
import pytest
from numpy import dtype

from transformations.standard_transformations import date_format_standard


@pytest.mark.xfail(
    run=False, reason="If we return a datetime object this will break " "the db insert"
)
def test_date_format_standard():
    test_data = {"should_be_a_date": ["2020-10-22"], "bonus_col": ["test "]}

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    result_df = date_format_standard(
        original_col="should_be_a_date", aggregate_col="now_a_date", df=test_data_df
    )

    print(result_df.to_markdown())
    print(list(result_df.dtypes))

    assert result_df.dtypes[1] == dtype("datetime64")
