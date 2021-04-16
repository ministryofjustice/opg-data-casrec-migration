from datetime import datetime

from pytest_cases import case
import pandas as pd


module_name = "bonds"
source_table = "order"
destination_table = "bonds"


@case(tags="simple")
def case_bonds_simple(test_config):
    simple_matches = {
        "Bond No.": ["bondreferencenumber"],
        "Bond Renewal": ["renewaldateofbond"],
        "Bond Discharge": ["dischargedate"],
    }
    merge_columns = {"source": "CoP Case", "transformed": "c_cop_case"}

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
    """

    return (simple_matches, merge_columns, source_query, transformed_query, module_name)


@case(tags="lookups")
def case_bonds_lookups(test_config):
    lookup_fields = {
        "bond_provider_id": {"Bond Co": "bond_provider_lookup"},
    }
    merge_columns = {"source": "CoP Case", "transformed": "c_cop_case"}

    config = test_config

    source_columns = list(set([f'"{y}"' for x in lookup_fields.values() for y in x]))
    transformed_columns = [f'"{x}"' for x in lookup_fields.keys()]

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
    """

    return (lookup_fields, merge_columns, source_query, transformed_query, module_name)


@case(tags="round")
def case_bonds_round(test_config):
    round_columns = {
        "Bond Amount": ["requiredbondamount"],
        "Bond Amt OPG": ["bondamounttaken"],
    }

    config = test_config
    merge_columns = {"source": "CoP Case", "transformed": "c_cop_case"}
    source_columns = [f'"{x}"' for x in round_columns.keys()]
    transformed_columns = [f'"{y}"' for x in round_columns.values() for y in x]

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
    """

    return (
        round_columns,
        source_query,
        transformed_query,
        merge_columns,
        module_name,
    )


@case(tags="one_to_one_joins")
def case_bonds_join(test_config):
    join_columns = {
        "order_id": {"cases": "id"},
    }
    merge_columns = {"fk_child": "c_cop_case", "fk_parent": "c_cop_case"}

    config = test_config

    fk_child_col = [f'"{k}"' for k in join_columns.keys()]

    parent_table = [y for x in join_columns.values() for y in x]

    fk_parent_col = [f'"{y}"' for x in join_columns.values() for y in x.values()]

    fk_child_query = f"""
        SELECT
            "{merge_columns['fk_child']}",
            {', '.join(fk_child_col)}
        FROM {config.schemas['post_transform']}.{destination_table}
    """

    fk_parent_query = f"""
            SELECT
                "{merge_columns['fk_parent']}",
                {', '.join(fk_parent_col)}
            FROM {config.schemas['post_transform']}.{parent_table[0]}
        """

    return (join_columns, merge_columns, fk_child_query, fk_parent_query, module_name)


@case(tags="row_count")
def case_bonds_count(test_config):

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
    """

    return (source_query, transformed_query, module_name)
