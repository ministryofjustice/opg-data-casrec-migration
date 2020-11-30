from pytest_cases import case


@case(id="do_simple_mapping called")
def case_do_simple_mapping():

    mapping = {
        "caserecnumber": {
            "alias": "Case",
            "casrec_column_name": "Case",
            "casrec_table": "ORDER",
            "default_value": "",
            "calculated": "",
            "requires_transformation": "",
            "lookup_table": [],
        }
    }

    log_message = "mock do_simple_mapping"

    return (mapping, log_message)


@case(id="do_simple_transformations called")
def case_do_simple_transformations():

    mapping = {
        "uid": {
            "alias": "",
            "casrec_column_name": "",
            "casrec_table": "",
            "default_value": "",
            "calculated": "",
            "requires_transformation": "unique_number",
            "lookup_table": [],
        },
    }

    log_message = "mock do_simple_transformations"

    return (mapping, log_message)


@case(id="add_required_columns called")
def case_add_required_columns():

    mapping = {
        "casetype": {
            "alias": "",
            "casrec_column_name": "",
            "casrec_table": "",
            "default_value": "ORDER",
            "calculated": "",
            "requires_transformation": "",
            "lookup_table": [],
        },
    }

    log_message = "mock add_required_columns"

    return (mapping, log_message)


@case(id="map_lookup_tables")
def case_map_lookup_tables():

    mapping = {
        "casetype": {
            "alias": "",
            "casrec_column_name": "",
            "casrec_table": "",
            "default_value": "ORDER",
            "calculated": "",
            "requires_transformation": "",
            "lookup_table": "accommodation_type_lookup",
        },
    }

    log_message = "mock map_lookup_tables"

    return (mapping, log_message)
