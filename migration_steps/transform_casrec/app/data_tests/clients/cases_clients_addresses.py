from pytest_cases import case

module_name = "client_addresses"
source_table = "pat"
destination_table = "addresses"


@case(tags="simple")
def case_clients_1(test_config):
    simple_matches = {
        "Adrs3": ["town"],
        "Adrs4": ["county"],
        "Postcode": ["postcode"],
        "Adrs5": ["country"],
    }
    merge_columns = {"source": "Case", "transformed": "caserecnumber"}

    config = test_config
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


#
#
@case(tags="default")
def case_clients_2(test_config):
    defaults = {
        "type": "Primary",
    }

    config = test_config
    source_columns = [f'"{x}"' for x in defaults.keys()]

    source_query = f"""
        SELECT
            {', '.join(source_columns)}
        FROM {config.etl2_schema}.{destination_table}
    """

    return (defaults, source_query, module_name)


@case(tags="convert_to_bool")
def case_clients_3(test_config):
    convert_to_bool_fields = {
        "Foreign": ["isairmailrequired"],
    }

    config = test_config
    merge_columns = {"source": "Case", "transformed": "c_case"}
    source_columns = [f'"{x}"' for x in convert_to_bool_fields.keys()]
    transformed_columns = [f'"{y}"' for x in convert_to_bool_fields.values() for y in x]

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

    return (
        convert_to_bool_fields,
        source_query,
        transformed_query,
        merge_columns,
        module_name,
    )


@case(tags="squash_columns")
def case_clients_4(test_config):
    squash_columns_fields = {
        "address_lines": ["Adrs1", "Adrs2"],
    }

    config = test_config
    merge_columns = {"source": "Case", "transformed": "c_case"}
    source_columns = [f'"{y}"' for x in squash_columns_fields.values() for y in x]
    transformed_columns = [f'"{x}"' for x in squash_columns_fields.keys()]

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

    return (
        squash_columns_fields,
        source_query,
        transformed_query,
        merge_columns,
        module_name,
    )


@case(tags="one_to_one_joins")
def case_clients_5(test_config):
    join_columns = {
        "person_id": {"persons": "id"},
    }
    merge_columns = {"fk_child": "c_case", "fk_parent": "caserecnumber"}

    config = test_config

    fk_child_col = [f'"{k}"' for k in join_columns.keys()]

    parent_table = [y for x in join_columns.values() for y in x]

    fk_parent_col = [f'"{y}"' for x in join_columns.values() for y in x.values()]

    fk_child_query = f"""
        SELECT
            "{merge_columns['fk_child']}",
            {', '.join(fk_child_col)}
        FROM {config.etl2_schema}.{destination_table}
    """

    fk_parent_query = f"""
            SELECT
                "{merge_columns['fk_parent']}",
                {', '.join(fk_parent_col)}
            FROM {config.etl2_schema}.{parent_table[0]}
        """

    return (join_columns, merge_columns, fk_child_query, fk_parent_query, module_name)


@case(tags="row_count")
def case_addresses_count(test_config):

    config = test_config
    source_query = f"""
        SELECT
            *
        FROM {config.etl1_schema}.{source_table}
    """

    transformed_query = f"""
        SELECT
            *
        FROM {config.etl2_schema}.{destination_table}
    """

    return (source_query, transformed_query, module_name)
