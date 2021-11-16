from utilities.standard_transformations import last_words
import pandas as pd
from pandas.util.testing import assert_frame_equal

def test_last_words():
    df = pd.DataFrame({
        'source':  ['one-word', 'two words', 'three wor ds'],
        'ignored-col': ['a', 'b', 'c'],
    })
    
    result_df = last_words('source', 'destination', df)

    assert_frame_equal(result_df, pd.DataFrame({
        'ignored-col': ['a', 'b', 'c'],
        'destination':  ['', 'words', 'wor ds'],
    }))
