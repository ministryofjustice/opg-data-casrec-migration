from pytest_cases import case


@case(id="do_simple_mapping called")
def case_do_simple_mapping():

    mapping = {
        "caserecnumber": {
            "alias": "Case",
            "casrec_column_name": "Case",
            "casrec_table": "ORDER",
            "default_value": "",
            "requires_transformation": "",
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
            "requires_transformation": "unique_number",
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
            "requires_transformation": "",
        },
    }

    log_message = "mock add_required_columns"

    return (mapping, log_message)
