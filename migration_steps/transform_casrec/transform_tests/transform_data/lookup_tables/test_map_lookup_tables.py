import pandas as pd

from transform_data.lookup_tables import map_lookup_tables

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
    "name": ["Buffy", "Willow", "Xander", "Giles", "Oz", "Dawn"],
    "salutation": ["1", "2", "3", "4", "3", "1000"],
}

expected_result_data_dict = {
    "name": ["Buffy", "Willow", "Xander", "Giles", "Oz", "Dawn"],
    "salutation": ["Miss", "Ms", "Mr", "Sir", "Mr", ""],
}

test_source_data_df = pd.DataFrame(
    test_source_data_dict, columns=[x for x in test_source_data_dict]
)

expected_result_data_df = pd.DataFrame(
    expected_result_data_dict, columns=[x for x in expected_result_data_dict]
)


def test_map_lookup_tables(mock_get_lookup_dict):
    transformed_df = map_lookup_tables(test_simple_mapping_dict, test_source_data_df)

    assert transformed_df.equals(expected_result_data_df)
