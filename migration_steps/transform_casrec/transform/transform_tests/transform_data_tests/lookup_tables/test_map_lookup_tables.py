import pytest
from pandas._testing import assert_frame_equal


import helpers


def test_map_lookup_tables(mock_get_lookup_dict):
    test_simple_mapping_dict = {
        "salutation": {
            "casrec_table": "PAT",
            "casrec_column_name": "Title",
            "alias": "Title",
            "requires_transformation": "",
            "lookup_table": "fake_titles_lookup",
            "default_value": "",
            "calculated": "",
        },
    }

    test_source_data_dict = {
        "name": ["Buffy", "Willow", "Xander", "Giles", "Oz", "Dawn", "Kendra"],
        "salutation": ["1", "2", "3", "4", "3", "1000", None],
    }

    expected_result_data_dict = {
        "name": ["Buffy", "Willow", "Xander", "Giles", "Oz", "Dawn", "Kendra"],
        "salutation": ["Miss", "Ms", "Mr", "Sir", "Mr", "", ""],
    }

    test_source_data_df = pd.DataFrame(
        test_source_data_dict, columns=[x for x in test_source_data_dict]
    )

    expected_result_data_df = pd.DataFrame(
        expected_result_data_dict, columns=[x for x in expected_result_data_dict]
    )

    transformed_df = map_lookup_tables(test_simple_mapping_dict, test_source_data_df)

    assert transformed_df.equals(expected_result_data_df)


import pandas as pd

from transform_data.lookup_tables import map_lookup_tables


@pytest.mark.xfail(reason="nulls not accounted for yet")
def test_map_lookup_tables_nulls(monkeypatch):
    test_simple_mapping_dict = {
        "correspondencebyemail": {
            "casrec_table": "deputy",
            "casrec_column_name": "By Email",
            "alias": "By Email",
            "requires_transformation": "",
            "lookup_table": "Corres_Indicator_lookup",
            "default_value": "",
            "calculated": "",
        },
    }

    test_source_data_dict = {
        "id": [1, 2, 3, 4, 5],
        "correspondencebyemail": ["Y", "N", "Y", "N", None],
    }

    expected_result_data_dict = {
        "id": [1, 2, 3, 4, 5],
        "correspondencebyemail": [True, False, True, False, None],
    }

    test_source_data_df = pd.DataFrame(
        test_source_data_dict, columns=[x for x in test_source_data_dict]
    )

    expected_result_data_df = pd.DataFrame(
        expected_result_data_dict, columns=[x for x in expected_result_data_dict]
    )

    def mock_lookup_dict(*args, **kwargs):
        print("using mock_lookup_dict for Corres_Indicator_lookup")
        mock_lookup_dict = {"Y": True, "N": False}
        return mock_lookup_dict

    monkeypatch.setattr(helpers, "get_lookup_dict", mock_lookup_dict)

    transformed_df = map_lookup_tables(test_simple_mapping_dict, test_source_data_df)

    print(f"\n{expected_result_data_df.to_markdown()}")
    print(f"\n{transformed_df.to_markdown()}")

    assert_frame_equal(transformed_df, expected_result_data_df)


def test_map_lookup_tables_with_default_value(mock_get_lookup_dict):
    test_simple_mapping_dict = {
        "salutation": {
            "casrec_table": "PAT",
            "casrec_column_name": "Title",
            "alias": "Title",
            "requires_transformation": "",
            "lookup_table": "fake_titles_lookup",
            "default_value": "Captain",
            "calculated": "",
        },
    }

    test_source_data_dict = {
        "name": ["Buffy", "Willow", "Xander", "Giles", "Oz", "Dawn", "Kendra"],
        "salutation": ["1", "2", "3", "4", "3", "1000", None],
    }

    expected_result_data_dict = {
        "name": ["Buffy", "Willow", "Xander", "Giles", "Oz", "Dawn", "Kendra"],
        "salutation": ["Miss", "Ms", "Mr", "Sir", "Mr", "Captain", "Captain"],
    }

    test_source_data_df = pd.DataFrame(
        test_source_data_dict, columns=[x for x in test_source_data_dict]
    )

    expected_result_data_df = pd.DataFrame(
        expected_result_data_dict, columns=[x for x in expected_result_data_dict]
    )

    transformed_df = map_lookup_tables(test_simple_mapping_dict, test_source_data_df)

    assert transformed_df.equals(expected_result_data_df)
