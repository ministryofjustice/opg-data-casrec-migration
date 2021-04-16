import json

from pytest_cases import case
import pandas as pd


@case(id="squashable column data is as expected")
def case_data_as_expected():
    test_data = {
        "column_1": ["some "],
        "column_2": ["test "],
        "column_3": ["data"],
        "column_4": ["unsquashed"],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    cols_to_squash = ["column_1", "column_2", "column_3"]
    new_col = "squashed"

    expected_result_dict = {
        "column_4": ["unsquashed"],
        "squashed": json.dumps(["some ", "test ", "data"]),
    }

    expected_result = pd.DataFrame(
        expected_result_dict, columns=[x for x in expected_result_dict]
    )

    return (
        test_data_df,
        cols_to_squash,
        new_col,
        expected_result,
    )


@case(id="squashable column data has an empty value")
def case_data_empty():
    test_data = {
        "column_1": ["some "],
        "column_2": [""],
        "column_3": ["data"],
        "column_4": ["unsquashed"],
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    cols_to_squash = ["column_1", "column_2", "column_3"]
    new_col = "squashed"

    expected_result_dict = {
        "column_4": ["unsquashed"],
        "squashed": json.dumps(["some ", "", "data"]),
    }

    expected_result = pd.DataFrame(
        expected_result_dict, columns=[x for x in expected_result_dict]
    )

    return (
        test_data_df,
        cols_to_squash,
        new_col,
        expected_result,
    )
