import pandas as pd


from transformations.transformations_from_mapping import add_required_columns


def test_add_required_columns():
    required_columns = {
        "new_required_1": {"data_type": "bool", "default_value": False},
        "new_required_2": {"data_type": "bool", "default_value": 1},
        "new_required_3": {"data_type": "str", "default_value": "default_value_3"},
    }

    test_data = {
        "column_1": [str(x) for x in range(0, 10)],
        "column_2": [str(x * x) for x in range(0, 10)],
        "column_3": [str(x * x * x) for x in range(0, 10)],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    result_df = add_required_columns(required_columns, test_data_df)

    assert [x for x in test_data] + list(
        required_columns.keys()
    ) == result_df.columns.values.tolist()

    assert result_df.sample()["new_required_1"].values == False
    assert result_df.sample()["new_required_2"].values == 1
    assert result_df.sample()["new_required_3"].values == "default_value_3"
