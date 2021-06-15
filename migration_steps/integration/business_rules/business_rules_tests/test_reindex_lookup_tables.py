import pandas as pd

from rules import reindex_lookups
from rules.reindex_lookups import get_sirius_lookup_data, generate_updates


def test_get_lookups_to_reindex():
    result = reindex_lookups.get_lookups_to_reindex()

    expected_result = {
        "bonds": [
            {"bond_provider_id": {"bond_provider_lookup": "bond_providers"}},
        ]
    }
    assert result == expected_result


def test_generate_sirius_lookup_remap(monkeypatch):

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
    test_lookup_field = "uid"
    test_result_field = "id"
    test_df = sirius_data_df

    expected_result = {"HOWDEN": 66, "DBS": 77, "MARSH": 88, "OTHER": 99}

    result = reindex_lookups.generate_sirius_lookup_remap(
        lookup_field=test_lookup_field, result_field=test_result_field, df=test_df
    )

    assert result == expected_result


def test_generate_updates():

    test_lookup_remap = {"HOWDEN": 66, "DBS": 77, "MARSH": 88, "OTHER": 99}
    test_schema = "fake_sirius"
    test_table = "pretend_table"
    test_field_to_reindex = "reindex_me"

    expected_result = [
        "UPDATE fake_sirius.pretend_table set reindex_me = 66 where reindex_me = 'HOWDEN';",
        "UPDATE fake_sirius.pretend_table set reindex_me = 77 where reindex_me = 'DBS';",
        "UPDATE fake_sirius.pretend_table set reindex_me = 88 where reindex_me = 'MARSH';",
        "UPDATE fake_sirius.pretend_table set reindex_me = 99 where reindex_me = 'OTHER';",
    ]

    result = generate_updates(
        lookup_remap=test_lookup_remap,
        schema=test_schema,
        table=test_table,
        field_to_reindex=test_field_to_reindex,
    )

    assert result == expected_result
