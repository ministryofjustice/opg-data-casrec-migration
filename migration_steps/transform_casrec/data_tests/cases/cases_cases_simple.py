from pytest_cases import case


@case(tags="simple")
def case_cases(get_config):
    simple_matches = {"Ord Type": "ordersubtype", "Case": "caserecnumber"}
    merge_columns = {"source": "Order No", "transformed": "c_order_no"}

    config = get_config
    source_columns = [f'"{x}"' for x in simple_matches.keys()]
    transformed_columns = [f'"{x}"' for x in simple_matches.values()]

    source_query = f"""
        SELECT
            "{merge_columns['source']}",
            {', '.join(source_columns)}
        FROM {config.etl1_schema}.order
    """

    transformed_query = f"""
        SELECT
            {merge_columns['transformed']},
            {', '.join(transformed_columns)}
        FROM {config.etl2_schema}.cases
    """

    return (simple_matches, merge_columns, source_query, transformed_query)
