from utilities.standard_transformations import capitalise_first_letter
import pandas as pd
from pandas.util.testing import assert_frame_equal


def test_capitalise_first_letter():
    df = pd.DataFrame(
        {
            "source": ["first", "first-Second", "first Second", ""],
            "ignored-col": ["a", "b", "c", "d"],
        }
    )

    result_df = capitalise_first_letter("source", "destination", df)

    assert_frame_equal(
        result_df,
        pd.DataFrame(
            {
                "ignored-col": ["a", "b", "c", "d"],
                "destination": ["First", "First-second", "First second", ""],
            }
        ),
    )
