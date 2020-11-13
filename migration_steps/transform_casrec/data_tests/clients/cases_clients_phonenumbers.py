from pytest_cases import case

module_name = "client_phonenumbers"
source_table = "pat"
destination_table = "phonenumbers"


@case(tags="simple")
def case_clients_phonenos_1(get_config):
    simple_matches = {
        "Client Phone": ["phone_number"],
    }
    merge_columns = {"source": "Case", "transformed": "caserecnumber"}

    config = get_config

    source_columns = [f'"{x}"' for x in simple_matches.keys()]
    transformed_columns = [f'"{y}"' for x in simple_matches.values() for y in x]

    source_query = f"""
        SELECT
            "{merge_columns['source']}",
            {', '.join(source_columns)}
        FROM {config.etl1_schema}.{source_table}
    """

    transformed_query = f"""
        SELECT
            {merge_columns['transformed']},
            {', '.join(transformed_columns)}
        FROM {config.etl2_schema}.{destination_table}
    """

    return (simple_matches, merge_columns, source_query, transformed_query, module_name)


@case(tags="default")
def case_clients_phonenos_2(get_config):
    defaults = {
        "type": "Home",
        "is_default": False,
        "updateddate": "Todays Date",
    }

    config = get_config
    source_columns = [f'"{x}"' for x in defaults.keys()]

    source_query = f"""
        SELECT
            {', '.join(source_columns)}
        FROM {config.etl2_schema}.{destination_table}
    """

    return (defaults, source_query, module_name)
