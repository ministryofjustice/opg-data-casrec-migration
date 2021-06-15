import pandas as pd

from rules import convert_datatypes


def test_get_lookups_to_convert():
    result = convert_datatypes.get_cols_to_convert()

    expected_result = {
        "bonds": [
            {"bond_provider_id": "int"},
        ]
    }
    assert result == expected_result
