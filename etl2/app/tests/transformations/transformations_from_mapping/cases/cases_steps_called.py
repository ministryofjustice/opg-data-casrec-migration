from pytest_cases import case


@case(id="do_simple_mapping called")
def case_do_simple_mapping():

    mapping = {
        "simple_mapping": {"item1": "data"},
        "transformations": {},
        "required_columns": {},
    }

    log_message = "mock do_simple_mapping"

    return (mapping, log_message)


@case(id="do_simple_transformations called")
def case_do_simple_transformations():
    mapping = {
        "simple_mapping": {},
        "transformations": {"item1": "data"},
        "required_columns": {},
    }

    log_message = "mock do_simple_transformations"

    return (mapping, log_message)


@case(id="add_required_columns called")
def case_add_required_columns():
    mapping = {
        "simple_mapping": {},
        "transformations": {},
        "required_columns": {"item1": "data"},
    }
    log_message = "mock add_required_columns"

    return (mapping, log_message)


@case(id="add_unique_id called")
def case_add_unique_id():
    mapping = {"simple_mapping": {}, "transformations": {}, "required_columns": {}}

    log_message = "mock add_unique_id"

    return (mapping, log_message)
