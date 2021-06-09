import pandas as pd

from rules.reindex_lookups import get_lookups_to_reindex


def test_get_lookups_to_reindex():
    result = get_lookups_to_reindex()

    expected_result = {
        "bonds_mapping": [
            {"dischargedate": "discharge_lookup"},
            {"bond_provider_id": "bond_provider_lookup"},
        ]
    }

    assert result == expected_result
