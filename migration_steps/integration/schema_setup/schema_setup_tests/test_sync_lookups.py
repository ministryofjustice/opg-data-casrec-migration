import pandas as pd

import helpers
from lookups import sync_lookups_in_staging
from lookups import check_lookups_in_mapping


def test_get_lookups_to_sync():
    result = sync_lookups_in_staging.get_lookups_to_sync()

    expected_result = {
        "bonds": [
            {"bond_provider_id": {"bond_provider_lookup": "bond_providers"}},
        ]
    }
    assert result == expected_result


def test_check_single_lookup_true(monkeypatch):
    def mock_get_sirius_data(*args, **kwargs):
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

    def mock_get_lookup_dict(*args, **kwargs):
        lookup_data = {1: 66, 2: 77, 3: 88}
        return lookup_data

    monkeypatch.setattr(
        check_lookups_in_mapping, "get_sirius_data", mock_get_sirius_data
    )
    monkeypatch.setattr(helpers, "get_lookup_dict", mock_get_lookup_dict)

    expected_result = True

    result = check_lookups_in_mapping.check_single_lookup(
        db_config={}, table="test", lookup_file_name="test"
    )

    assert result == expected_result


def test_check_single_lookup_false(monkeypatch):
    def mock_get_sirius_data(*args, **kwargs):
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

    def mock_get_lookup_dict(*args, **kwargs):
        lookup_data = {1: 666, 2: 777, 3: 888}
        return lookup_data

    monkeypatch.setattr(
        check_lookups_in_mapping, "get_sirius_data", mock_get_sirius_data
    )
    monkeypatch.setattr(helpers, "get_lookup_dict", mock_get_lookup_dict)

    expected_result = False

    result = check_lookups_in_mapping.check_single_lookup(
        db_config={}, table="test", lookup_file_name="test"
    )

    assert result == expected_result
