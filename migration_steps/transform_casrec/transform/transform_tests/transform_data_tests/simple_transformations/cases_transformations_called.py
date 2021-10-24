from pytest_cases import case


@case(id="squash_columns called")
def case_squash():
    test_transformations = {
        "squash_columns": [
            {
                "original_columns": ["Dep Adrs1", "Dep Adrs2", "Dep Adrs3"],
                "aggregate_col": "address_lines",
            }
        ],
    }

    log_message = "mock squash_columns"

    return (test_transformations, log_message)


@case(id="convert_to_bool called")
def case_bool():
    test_transformations = {
        "convert_to_bool": [
            {
                "original_columns": ["Dep Adrs1", "Dep Adrs2", "Dep Adrs3"],
                "aggregate_col": "address_lines",
            }
        ],
    }

    log_message = "mock convert_to_bool"

    return (test_transformations, log_message)


@case(id="unique_number called")
def case_unique():
    test_transformations = {
        "unique_number": [
            {
                "original_columns": ["Dep Adrs1", "Dep Adrs2", "Dep Adrs3"],
                "aggregate_col": "address_lines",
            }
        ],
    }

    log_message = "mock unique_number"

    return (test_transformations, log_message)
