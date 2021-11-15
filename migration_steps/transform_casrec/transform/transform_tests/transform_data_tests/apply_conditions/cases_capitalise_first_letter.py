from pytest_cases import case
import pandas as pd


case(id="bring back capitalised strings")


def case_less_than():
    test_data = {
        "c_test_col": ["BOB", "mary-Jane", "hecTor Hamster", ""],
    }
    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    conditions = {"capitalise_first_letter": {"cols": ["c_test_col"]}}

    expected_data = {
        "c_test_col": ["Bob", "Mary-jane", "Hector hamster", ""],
    }
    expected_result_data_data_df = pd.DataFrame(
        expected_data, columns=[x for x in expected_data]
    )

    return (test_data_df, conditions, expected_result_data_data_df)
