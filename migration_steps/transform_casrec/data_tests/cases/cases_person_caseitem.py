from pytest_cases import case


module_name = "person_caseitem"

source_tables = {"parent": "pat", "child": "order"}

destination_tables = {
    "parent": "persons",
    "child": "cases",
    "join_table": "person_caseitem",
}


@case(tags="many_to_one_join")
def case_person_caseitem(get_config):

    merge_columns = {"source": "Case", "transformed": "caserecnumber"}

    config = get_config

    source_query = f"""
        SELECT
            {source_tables['parent']}."{merge_columns['source']}",
            count("{source_tables['child']}".*) as {source_tables['child']}_count
        FROM {config.etl1_schema}.{source_tables['parent']}
        LEFT OUTER JOIN {config.etl1_schema}."{source_tables['child']}"
            ON {source_tables['parent']}."Case" = "{source_tables['child']}"."Case"
        GROUP BY {source_tables['parent']}."{merge_columns['source']}"
    """

    transformed_query = f"""
        SELECT
            {destination_tables['parent']}.{merge_columns['transformed']},
            {destination_tables['parent']}.id as {destination_tables['parent']}_id,
            count({destination_tables['child']}.id) as {destination_tables['child']}_count
        FROM {config.etl2_schema}.{destination_tables['parent']}
        LEFT OUTER JOIN {config.etl2_schema}.{destination_tables['join_table']}
            on cast({destination_tables['join_table']}.person_id as int)
                = cast({destination_tables['parent']}.id as int)
        LEFT OUTER JOIN {config.etl2_schema}.{destination_tables['child']}
            on cast({destination_tables['join_table']}.case_id as int)
                = cast({destination_tables['child']}.id as int)
        WHERE {destination_tables['parent']}."type" = 'actor_client'
        GROUP BY {destination_tables['parent']}_id, {destination_tables['parent']}.{merge_columns['transformed']}
    """

    match_columns = {
        f"{destination_tables['child']}_count": f"{source_tables['child']}_count"
    }

    return module_name, source_query, transformed_query, merge_columns, match_columns
