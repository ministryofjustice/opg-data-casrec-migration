from pytest_cases import case


@case(tags="simple")
def case_clients_1(get_config):
    simple_matches = {
        "Adrs3": ["town"],
        "Adrs4": ["county"],
        "Postcode": ["postcode"],
        "Adrs5": ["country"],
    }
    merge_columns = {"source": "Case", "transformed": "caserecnumber"}

    config = get_config
    source_columns = [f'"{x}"' for x in simple_matches.keys()]
    transformed_columns = [f'"{y}"' for x in simple_matches.values() for y in x]

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
        FROM {config.etl2_schema}.addresses
    """

    return (simple_matches, merge_columns, source_query, transformed_query)


#
#
@case(tags="default")
def case_clients_2(get_config):
    defaults = {
        "type": "Primary",
    }

    config = get_config
    source_columns = [f'"{x}"' for x in defaults.keys()]

    source_query = f"""
        SELECT
            {', '.join(source_columns)}
        FROM {config.etl2_schema}.addresses
    """

    return (defaults, source_query)


@case(tags="convert_to_bool")
def case_clients_3(get_config):
    convert_to_bool_fields = {
        "Foreign": ["isairmailrequired"],
    }

    config = get_config
    merge_columns = {"source": "Case", "transformed": "c_case"}
    source_columns = [f'"{x}"' for x in convert_to_bool_fields.keys()]
    transformed_columns = [f'"{y}"' for x in convert_to_bool_fields.values() for y in x]

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
        FROM {config.etl2_schema}.addresses
    """

    return (convert_to_bool_fields, source_query, transformed_query, merge_columns)
