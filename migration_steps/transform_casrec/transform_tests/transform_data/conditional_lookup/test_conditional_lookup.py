import helpers

import pandas as pd

from transform_data.conditional_lookups import conditional_lookup

test_data = {
    "id": [1, 2, 3, 4, 5],
    "Term Date": ["2020-01-01", "2020-02-02", "2020-03-03", "2020-04-04", "2020-05-05"],
    # "Term Type": ['D', 'E', '', '0', 'd'],
    "c_term_type": ["D", "E", "", "0", "d"],
    "Status": ["Dead", "Out of cash", "n/a", "who can say", "Dead"],
}

test_source_data_df = pd.DataFrame(test_data, columns=[x for x in test_data])


expected_data = {
    "id": [1, 2, 3, 4, 5],
    "dateofdeath": ["2020-01-01", "", "", "", "2020-05-05"],
    "Status": ["Dead", "Out of cash", "n/a", "who can say", "Dead"],
}

expected_data_df = pd.DataFrame(expected_data, columns=[x for x in expected_data])

lookup_file_name = "fake_lookup_file"
lookup_col = "Term Type"
final_col = "dateofdeath"
data_col = "Term Date"


def test_conditional_lookup(mock_get_lookup_dict_conditional):

    result = conditional_lookup(
        final_col=final_col,
        lookup_col=lookup_col,
        data_col=data_col,
        lookup_file_name=lookup_file_name,
        df=test_source_data_df,
    )

    print(f"\n{result.to_markdown()}")
