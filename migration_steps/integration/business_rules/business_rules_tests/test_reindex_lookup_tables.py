import pandas as pd

from rules import reindex_lookups


def test_get_lookups_to_reindex():
    result = reindex_lookups.get_lookups_to_reindex()

    expected_result = {
        "bonds": [
            {"dischargedate": "discharge_lookup"},
            {"bond_provider_id": "bond_provider_lookup"},
        ]
    }
    assert result == expected_result


def test_reindex_single_lookup(monkeypatch):
    def mock_get_lookup_data(*args, **kwargs):

        sirius_data = {
            "id": [66, 77, 88, 99],
            "name": ["Howden", "Deputy Bond Services (DBS)", "Marsh", "Other"],
            "oneoffvalue": [21000, 21000, 16000, None],
            "telephonenumber": [None, None, None, None],
            "emailaddress": [None, None, None, None],
            "webaddress": [
                "https://www.howdendeputybonds.co.uk",
                "https://www.deputybondservices.co.uk",
                None,
                None,
            ],
            "uid": ["HOWDEN", "DBS", "MARSH", "OTHER"],
        }

        sirius_data_df = pd.DataFrame(sirius_data, columns=[x for x in sirius_data])

        return sirius_data_df

    monkeypatch.setattr(reindex_lookups, "get_sirius_data", mock_get_lookup_data)

    reindex_lookups.reindex_single_lookup()

    assert 1 == 5
