from transformations.transformations_from_mapping import (
    get_simple_mapping,
    get_transformations,
    get_default_values,
)


test_mapping = {
    "caserecnumber": {
        "casrec_table": "ORDER",
        "casrec_column_name": "Case",
        "alias": "Case",
        "requires_transformation": "",
        "default_value": "",
        "test_comments": "standard column",
    },
    "uid": {
        "casrec_table": "",
        "casrec_column_name": "",
        "alias": "",
        "requires_transformation": "unique_number",
        "default_value": "",
        "test_comments": "has 'unique_number' transformation",
    },
    "another_uid": {
        "casrec_table": "",
        "casrec_column_name": "",
        "alias": "",
        "requires_transformation": "unique_number",
        "default_value": "",
        "test_comments": "repeated 'unique_number' transformation",
    },
    "type": {
        "casrec_table": "",
        "casrec_column_name": "",
        "alias": "",
        "requires_transformation": "",
        "default_value": "order",
        "test_comments": "has a default value",
    },
    "orderdate": {
        "casrec_table": "ORDER",
        "casrec_column_name": "Made Date",
        "alias": "Made Date",
        "requires_transformation": "",
        "default_value": "",
        "test_comments": "standard column",
    },
    "orderexpirydate": {
        "casrec_table": "ORDER",
        "casrec_column_name": "Made Date",
        "alias": "Made Date 1",
        "requires_transformation": "",
        "default_value": "",
        "test_comments": "repeated column name",
    },
    "dob": {
        "casrec_table": "PAT",
        "casrec_column_name": "DOB",
        "alias": "DOB",
        "requires_transformation": "date_format_standard",
        "default_value": "",
        "test_comments": "has 'date_format_standard' transformation",
    },
}


expected_simple_mapping_dict = {
    "caserecnumber": {
        "casrec_table": "ORDER",
        "casrec_column_name": "Case",
        "alias": "Case",
        "requires_transformation": "",
        "default_value": "",
        "test_comments": "standard column",
    },
    "orderdate": {
        "casrec_table": "ORDER",
        "casrec_column_name": "Made Date",
        "alias": "Made Date",
        "requires_transformation": "",
        "default_value": "",
        "test_comments": "standard column",
    },
    "orderexpirydate": {
        "casrec_table": "ORDER",
        "casrec_column_name": "Made Date",
        "alias": "Made Date 1",
        "requires_transformation": "",
        "default_value": "",
        "test_comments": "repeated column name",
    },
    "dob": {
        "casrec_table": "PAT",
        "casrec_column_name": "DOB",
        "alias": "DOB",
        "requires_transformation": "date_format_standard",
        "default_value": "",
        "test_comments": "has 'date_format_standard' transformation",
    },
}

expected_default_values_dict = {
    "type": {
        "casrec_table": "",
        "casrec_column_name": "",
        "alias": "",
        "requires_transformation": "",
        "default_value": "order",
        "test_comments": "has a default value",
    },
}


expected_transformations_dict_2 = {
    "unique_number": [
        {"original_columns": "", "aggregate_col": "uid",},
        {"original_columns": "", "aggregate_col": "another_uid",},
    ],
}


def test_get_simple_mapping():

    result = get_simple_mapping(mapping_definitions=test_mapping)
    assert result == expected_simple_mapping_dict


def test_get_default_values():

    result = get_default_values(mapping_definitions=test_mapping)
    assert result == expected_default_values_dict


def test_get_transformations():

    result = get_transformations(mapping_definitions=test_mapping)
    assert result == expected_transformations_dict_2
