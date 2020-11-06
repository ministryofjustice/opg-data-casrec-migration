from pytest_cases import case


@case(tags="simple")
def case_clients(get_config):
    simple_matches = {
        "Forename": "firstname",
        "Surname": "surname",
        "Title": "salutation",
        "Create": "createddate",
    }
    merge_columns = {"source": "Case", "transformed": "caserecnumber"}

    config = get_config
    source_columns = [f'"{x}"' for x in simple_matches.keys()]
    transformed_columns = [f'"{x}"' for x in simple_matches.values()]

    source_query = f"""
        SELECT
            "{merge_columns['source']}",
            {', '.join(source_columns)}
        FROM {config.etl1_schema}.pat
    """

    transformed_query = f"""
        SELECT
            {merge_columns['transformed']},
            {', '.join(transformed_columns)}
        FROM {config.etl2_schema}.persons
        WHERE "type" = 'actor_client'
    """

    return (simple_matches, merge_columns, source_query, transformed_query)
