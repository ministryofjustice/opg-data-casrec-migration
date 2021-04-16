import pytest
from pytest_cases import case


module_name = "person_caseitem"

source_tables = {"parent": "pat", "child": "order"}

destination_tables = {
    "parent": "persons",
    "child": "cases",
    "join_table": "person_caseitem",
}
json_files = {"parent": "client_persons_mapping", "child": "cases_mapping"}


@case(tags="many_to_one_join")
def case_person_caseitem(test_config):

    merge_columns = {"source": "Case", "transformed": "caserecnumber"}

    config = test_config

    source_query = f"""
        SELECT
            {source_tables['parent']}."{merge_columns['source']}",
            count("{source_tables['child']}".*) as {source_tables['child']}_count
        FROM {config.schemas['pre_transform']}.{source_tables['parent']}
        LEFT OUTER JOIN {config.schemas['pre_transform']}."{source_tables['child']}"
            ON {source_tables['parent']}."Case" = "{source_tables['child']}"."Case"
        GROUP BY {source_tables['parent']}."{merge_columns['source']}"
    """

    transformed_query = f"""
        SELECT
            {destination_tables['parent']}.{merge_columns['transformed']},
            {destination_tables['parent']}.id as {destination_tables['parent']}_id,
            count({destination_tables['child']}.id) as {destination_tables['child']}_count
        FROM {config.schemas['post_transform']}.{destination_tables['parent']}
        LEFT OUTER JOIN {config.schemas['post_transform']}.{destination_tables['join_table']}
            on cast({destination_tables['join_table']}.person_id as int)
                = cast({destination_tables['parent']}.id as int)
        LEFT OUTER JOIN {config.schemas['post_transform']}.{destination_tables['child']}
            on cast({destination_tables['join_table']}.caseitem_id as int)
                = cast({destination_tables['child']}.id as int)
            AND {destination_tables['child']}.casrec_mapping_file_name = '{json_files['child']}'
        WHERE {destination_tables['parent']}.casrec_mapping_file_name = '{json_files['parent']}'
        GROUP BY {destination_tables['parent']}_id, {destination_tables['parent']}.{merge_columns['transformed']}
    """

    match_columns = {
        f"{destination_tables['child']}_count": f"{source_tables['child']}_count"
    }

    return module_name, source_query, transformed_query, merge_columns, match_columns


@case(tags="row_count")
def case_cases_count(test_config):
    # every case should be linked to a person
    config = test_config
    source_query = f"""
        SELECT
            *
        FROM {config.schemas['post_transform']}.{destination_tables['child']}
    """

    transformed_query = f"""
        SELECT
            distinct caseitem_id
        FROM {config.schemas['post_transform']}.{destination_tables['join_table']}
    """

    return (source_query, transformed_query, module_name)
