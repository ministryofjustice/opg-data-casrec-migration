from utilities.basic_data_table import get_source_table


def test_get_source_table():
    test_mapping_dict = {
        "id": {
            "casrec_table": "test_table",
            "casrec_column_name": "",
            "alias": "",
            "requires_transformation": "",
            "lookup_table": "",
            "default_value": "",
            "calculated": "",
            "additional_columns": "",
        },
        "person_id": {
            "casrec_table": "test_table",
            "casrec_column_name": "",
            "alias": "",
            "requires_transformation": "",
            "lookup_table": "",
            "default_value": "",
            "calculated": "",
            "additional_columns": "Case",
        },
    }
    expected_result = "test_table"

    result = get_source_table(mapping_dict=test_mapping_dict)

    assert result == expected_result


def test_get_source_table_multiple_tables():
    test_mapping_dict = {
        "id": {
            "casrec_table": "test_table",
            "casrec_column_name": "",
            "alias": "",
            "requires_transformation": "",
            "lookup_table": "",
            "default_value": "",
            "calculated": "",
            "additional_columns": "",
        },
        "person_id": {
            "casrec_table": "test_table_2",
            "casrec_column_name": "",
            "alias": "",
            "requires_transformation": "",
            "lookup_table": "",
            "default_value": "",
            "calculated": "",
            "additional_columns": "Case",
        },
    }
    expected_result = ""

    result = get_source_table(mapping_dict=test_mapping_dict)

    assert result == expected_result


def test_get_source_table_empty_tables():
    test_mapping_dict = {
        "id": {
            "casrec_table": "test_table",
            "casrec_column_name": "",
            "alias": "",
            "requires_transformation": "",
            "lookup_table": "",
            "default_value": "",
            "calculated": "",
            "additional_columns": "",
        },
        "person_id": {
            "casrec_table": "",
            "casrec_column_name": "",
            "alias": "",
            "requires_transformation": "",
            "lookup_table": "",
            "default_value": "",
            "calculated": "",
            "additional_columns": "Case",
        },
    }
    expected_result = "test_table"

    result = get_source_table(mapping_dict=test_mapping_dict)

    assert result == expected_result
