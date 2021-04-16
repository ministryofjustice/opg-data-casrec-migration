from pytest_cases import case
import pandas as pd


true_values = {
    "decimal as string": "1.0",
}
false_values = {"decimal as string": "6.0"}


@case(id="correct TRUE boolean values applied")
def case_correct_bool_values_true():
    test_data = {
        "should_be_bool": list(true_values.values()),
        "name": list(true_values.keys()),
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    original_col = "should_be_bool"
    new_col = "now_a_bool"

    expected_result_dict = {
        "name": list(true_values.keys()),
        "now_a_bool": [True for x in range(0, len(true_values))],
    }

    expected_result = pd.DataFrame(
        expected_result_dict, columns=[x for x in expected_result_dict]
    )

    return (
        test_data_df,
        original_col,
        new_col,
        expected_result,
    )


@case(id="correct FALSE boolean values applied")
def case_correct_bool_values_false():
    test_data = {
        "should_be_bool": list(false_values.values()),
        "name": list(false_values.keys()),
    }

    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    original_col = "should_be_bool"
    new_col = "now_a_bool"

    expected_result_dict = {
        "name": list(false_values.keys()),
        "now_a_bool": [False for x in range(0, len(false_values))],
    }

    expected_result = pd.DataFrame(
        expected_result_dict, columns=[x for x in expected_result_dict]
    )

    return (
        test_data_df,
        original_col,
        new_col,
        expected_result,
    )
