from datetime import datetime

import pytest
from pytest_cases import case
import pandas as pd

module_name = "client_phonenumbers_mapping"
source_table = "pat"
destination_table = "phonenumbers"


@case(tags="simple")
def case_clients_phonenos_1(test_config):
    simple_matches = {
        "Client Phone": ["phone_number"],
    }
    merge_columns = {"source": "Case", "transformed": "caserecnumber"}

    config = test_config

    source_columns = [f'"{x}"' for x in simple_matches.keys()]
    transformed_columns = [f'"{y}"' for x in simple_matches.values() for y in x]

    source_query = f"""
        SELECT
            "{merge_columns['source']}",
            {', '.join(source_columns)}
        FROM {config.schemas['pre_transform']}.{source_table}
    """

    transformed_query = f"""
        SELECT
            {merge_columns['transformed']},
            {', '.join(transformed_columns)}
        FROM {config.schemas['post_transform']}.{destination_table}
        WHERE casrec_mapping_file_name = '{module_name}'
    """

    return (simple_matches, merge_columns, source_query, transformed_query, module_name)


@case(tags="default")
def case_clients_phonenos_2(test_config):
    defaults = {
        "type": "Home",
        "is_default": False,
    }

    config = test_config
    source_columns = [f'"{x}"' for x in defaults.keys()]

    source_query = f"""
        SELECT
            {', '.join(source_columns)}
        FROM {config.schemas['post_transform']}.{destination_table}
        WHERE casrec_mapping_file_name = '{module_name}'
    """
    return (defaults, source_query, module_name)


@case(tags="calculated")
def case_clients_phonenos_3(test_config):
    today = pd.Timestamp.today()

    calculated_fields = {
        "updateddate": today,
    }

    config = test_config
    source_columns = [f'"{x}"' for x in calculated_fields.keys()]

    source_query = f"""
        SELECT
            {', '.join(source_columns)}
        FROM {config.schemas['post_transform']}.{destination_table}
        WHERE casrec_mapping_file_name = '{module_name}'
    """

    return (calculated_fields, source_query, module_name)


@case(tags="one_to_one_joins")
def case_clients_phonenos_joins(test_config):
    join_columns = {
        "person_id": {"persons": "id"},
    }
    merge_columns = {"fk_child": "c_case", "fk_parent": "caserecnumber"}

    config = test_config

    fk_child_col = [f'"{k}"' for k in join_columns.keys()]

    parent_table = [y for x in join_columns.values() for y in x]
    parent_module_name = "client_persons_mapping"

    fk_parent_col = [f'"{y}"' for x in join_columns.values() for y in x.values()]

    fk_child_query = f"""
        SELECT
            "{merge_columns['fk_child']}",
            {', '.join(fk_child_col)}
        FROM {config.schemas['post_transform']}.{destination_table}
        WHERE casrec_mapping_file_name = '{module_name}'

    """

    fk_parent_query = f"""
            SELECT
                "{merge_columns['fk_parent']}",
                {', '.join(fk_parent_col)}
            FROM {config.schemas['post_transform']}.{parent_table[0]}
            WHERE casrec_mapping_file_name = '{parent_module_name}'
        """

    return (join_columns, merge_columns, fk_child_query, fk_parent_query, module_name)


@case(tags="row_count")
def case_phonenumbers_count(test_config):

    config = test_config
    source_query = f"""
        SELECT
            *
        FROM {config.schemas['pre_transform']}.{source_table}
    """

    transformed_query = f"""
        SELECT
            *
        FROM {config.schemas['post_transform']}.{destination_table}
        WHERE casrec_mapping_file_name = '{module_name}'
    """

    return (source_query, transformed_query, module_name)
