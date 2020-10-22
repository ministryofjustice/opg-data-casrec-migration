from pytest_cases import case
import pandas as pd


@case(id="correct columns in result - drop original cols")
def case_drop_original_cols():
    test_data = {
        "column_1": ["some "],
        "column_2": ["test "],
        "column_3": ["data"],
        "column_4": ["unsquashed"],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    cols_to_squash = ["column_1", "column_2", "column_3"]
    new_col = "squashed"
    drop_original_cols = True

    result_column_list = ["column_4", "squashed"]

    return (
        test_data_df,
        cols_to_squash,
        new_col,
        drop_original_cols,
        result_column_list,
    )


@case(id="correct columns in result - keep original cols")
def case_keep_original_cols():
    test_data = {
        "column_1": ["some "],
        "column_2": ["test "],
        "column_3": ["data"],
        "column_4": ["unsquashed"],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    cols_to_squash = ["column_1", "column_2", "column_3"]
    new_col = "squashed"
    drop_original_cols = False

    result_column_list = ["column_1", "column_2", "column_3", "column_4", "squashed"]

    return (
        test_data_df,
        cols_to_squash,
        new_col,
        drop_original_cols,
        result_column_list,
    )
