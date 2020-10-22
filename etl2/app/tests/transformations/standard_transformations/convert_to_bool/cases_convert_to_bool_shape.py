import json

from pytest_cases import case
import pandas as pd


@case(id="correct columns in result - drop original cols")
def case_drop_original_cols():
    test_data = {
        "should_be_bool": ["1.0"],
        "bonus_col": ["pumpkins"],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    original_col = "should_be_bool"
    new_col = "now_a_bool"
    drop_original_col = True

    result_column_list = ["bonus_col", "now_a_bool"]

    return (
        test_data_df,
        original_col,
        new_col,
        drop_original_col,
        result_column_list,
    )


@case(id="correct columns in result - keep original cols")
def case_keep_original_cols():
    test_data = {
        "should_be_bool": ["1.0"],
        "bonus_col": ["pumpkins"],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    original_col = "should_be_bool"
    new_col = "now_a_bool"
    drop_original_col = False

    result_column_list = ["should_be_bool", "bonus_col", "now_a_bool"]

    return (
        test_data_df,
        original_col,
        new_col,
        drop_original_col,
        result_column_list,
    )
