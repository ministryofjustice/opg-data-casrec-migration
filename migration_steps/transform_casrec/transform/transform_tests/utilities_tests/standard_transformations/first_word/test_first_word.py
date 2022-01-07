from utilities.standard_transformations import first_word
import pandas as pd
from pandas.testing import assert_frame_equal


def test_first_word():
    df = pd.DataFrame(
        {
            "source": ["one-word", "one'word", "two words", "three wor ds"],
            "ignored-col": ["a", "b", "c", "d"],
        }
    )

    result_df = first_word("source", "destination", df)

    assert_frame_equal(
        result_df,
        pd.DataFrame(
            {
                "ignored-col": ["a", "b", "c", "d"],
                "destination": ["One-Word", "One'Word", "Two", "Three"],
            }
        ),
    )
