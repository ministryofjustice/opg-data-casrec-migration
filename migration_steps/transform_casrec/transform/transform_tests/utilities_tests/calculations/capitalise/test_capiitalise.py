from utilities.standard_transformations import capitalise
import pandas as pd


def test_capitalise():
    test_data = {
        "lower_case_col": [
            "i am lower case",
            "I have SOME capitAL letters",
            "I AM ALL CAPS",
        ],
        "expected_result": [
            "I AM LOWER CASE",
            "I HAVE SOME CAPITAL LETTERS",
            "I AM ALL CAPS",
        ],
    }
    test_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])

    result_df = capitalise(
        original_col="lower_case_col", result_col="caplitalised_col", df=test_data_df
    )

    assert result_df["caplitalised_col"].equals(result_df["expected_result"])
