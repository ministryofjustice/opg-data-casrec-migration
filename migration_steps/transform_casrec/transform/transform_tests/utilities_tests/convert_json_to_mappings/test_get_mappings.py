from utilities.convert_json_to_mappings import MappingDefinitions


test_mapping = {
    "caserecnumber": {
        "casrec_table": "ORDER",
        "casrec_column_name": "Case",
        "alias": "Case",
        "requires_transformation": "",
        "default_value": "",
        "calculated": "",
        "lookup_table": "",
        "test_comments": "standard column",
    },
    "uid": {
        "casrec_table": "",
        "casrec_column_name": "",
        "alias": "",
        "requires_transformation": "unique_number",
        "default_value": "",
        "calculated": "",
        "lookup_table": "",
        "test_comments": "has 'unique_number' transformation",
    },
    "another_uid": {
        "casrec_table": "",
        "casrec_column_name": "",
        "alias": "",
        "requires_transformation": "unique_number",
        "default_value": "",
        "calculated": "",
        "lookup_table": "",
        "test_comments": "repeated 'unique_number' transformation",
    },
    "type": {
        "casrec_table": "",
        "casrec_column_name": "",
        "alias": "",
        "requires_transformation": "",
        "default_value": "order",
        "calculated": "",
        "lookup_table": "",
        "test_comments": "has a default value",
    },
    "orderdate": {
        "casrec_table": "ORDER",
        "casrec_column_name": "Made Date",
        "alias": "Made Date",
        "requires_transformation": "",
        "default_value": "",
        "calculated": "",
        "lookup_table": "",
        "test_comments": "standard column",
    },
    "orderexpirydate": {
        "casrec_table": "ORDER",
        "casrec_column_name": "Made Date",
        "alias": "Made Date 1",
        "requires_transformation": "",
        "default_value": "",
        "calculated": "",
        "lookup_table": "",
        "test_comments": "repeated column name",
    },
    "dob": {
        "casrec_table": "PAT",
        "casrec_column_name": "DOB",
        "alias": "DOB",
        "requires_transformation": "date_format_standard",
        "default_value": "",
        "calculated": "",
        "lookup_table": "",
        "test_comments": "has 'date_format_standard' transformation",
    },
    "todays_date": {
        "casrec_table": "",
        "casrec_column_name": "",
        "alias": "",
        "requires_transformation": "",
        "default_value": "",
        "calculated": "current_date",
        "lookup_table": "",
        "test_comments": "has 'current_date' calculation",
    },
    "accomodation_type": {
        "casrec_table": "",
        "casrec_column_name": "",
        "alias": "",
        "requires_transformation": "",
        "default_value": "",
        "calculated": "",
        "lookup_table": "accomodation_type_lookup",
        "test_comments": "has a default value",
    },
    # "dateofdeath": {
    #     "casrec_table": "pat",
    #     "casrec_column_name": "Term Date",
    #     "alias": "",
    #     "requires_transformation": "",
    #     "default_value": "",
    #     "calculated": "conditional_lookup",
    #     "lookup_table": "death_lookup",
    #     "test_comments": "has a conditional lookup",
    # },
}


expected_simple_mapping_dict = {
    "caserecnumber": {
        "casrec_table": "ORDER",
        "casrec_column_name": "Case",
        "alias": "Case",
        "requires_transformation": "",
        "default_value": "",
        "calculated": "",
        "lookup_table": "",
        "test_comments": "standard column",
    },
    "orderdate": {
        "casrec_table": "ORDER",
        "casrec_column_name": "Made Date",
        "alias": "Made Date",
        "requires_transformation": "",
        "default_value": "",
        "calculated": "",
        "lookup_table": "",
        "test_comments": "standard column",
    },
    "orderexpirydate": {
        "casrec_table": "ORDER",
        "casrec_column_name": "Made Date",
        "alias": "Made Date 1",
        "requires_transformation": "",
        "default_value": "",
        "calculated": "",
        "lookup_table": "",
        "test_comments": "repeated column name",
    },
    "dob": {
        "casrec_table": "PAT",
        "casrec_column_name": "DOB",
        "alias": "DOB",
        "requires_transformation": "date_format_standard",
        "default_value": "",
        "calculated": "",
        "lookup_table": "",
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
        "calculated": "",
        "lookup_table": "",
        "test_comments": "has a default value",
    },
}


expected_transformations_dict = {
    "unique_number": [
        {
            "original_columns": "",
            "aggregate_col": "uid",
        },
        {
            "original_columns": "",
            "aggregate_col": "another_uid",
        },
    ],
}

expected_calculated_fields_dict = {
    "current_date": [
        {
            "column_name": "todays_date",
        },
    ],
    # "conditional_lookup": [
    #     {
    #         "column_name": "dateofdeath",
    #         "lookup_table": "death_lookup",
    #         "original_columns": "Term Date",
    #     },
    # ],
}


expected_lookup_values_dict = {
    "accomodation_type": {
        "casrec_table": "",
        "casrec_column_name": "",
        "alias": "",
        "requires_transformation": "",
        "default_value": "",
        "calculated": "",
        "lookup_table": "accomodation_type_lookup",
        "test_comments": "has a default value",
    },
}

mapping_defs = MappingDefinitions(mapping_definitions=test_mapping)
mappings = mapping_defs.generate_mapping_def()


def test_get_simple_mapping():

    # result = get_simple_mapping(mapping_definitions=test_mapping)
    result = mappings["simple_mapping"]
    assert result == expected_simple_mapping_dict


def test_get_default_values():

    # result = get_default_values(mapping_definitions=test_mapping)
    result = mappings["required_columns"]
    assert result == expected_default_values_dict


def test_get_transformations():

    # result = get_transformations(mapping_definitions=test_mapping)
    result = mappings["transformations"]
    assert result == expected_transformations_dict


def test_get_calculations():

    # result = get_calculations(mapping_definitions=test_mapping)
    result = mappings["calculated_fields"]
    assert result == expected_calculated_fields_dict


def test_get_lookup_tables():

    # result = get_lookup_tables(mapping_definitions=test_mapping)
    result = mappings["lookup_tables"]
    assert result == expected_lookup_values_dict
