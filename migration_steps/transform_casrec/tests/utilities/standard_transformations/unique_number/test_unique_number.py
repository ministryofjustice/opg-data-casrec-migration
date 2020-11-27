import pandas as pd

from utilities.standard_transformations import unique_number


def test_unique_number():
    new_col = "unique number column"

    test_data = {
        "column_1": [str(x) for x in range(0, 10)],
        "column_2": [str(x * x) for x in range(0, 10)],
        "column_3": [str(x * x * x) for x in range(0, 10)],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    result_df = unique_number(new_col, test_data_df)

    assert [x for x in test_data] + [new_col] == result_df.columns.values.tolist()
