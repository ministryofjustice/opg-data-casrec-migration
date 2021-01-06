from datetime import datetime

from pytest_cases import case
import pandas as pd


module_name = "supervision_level_log"
source_table = "order"
destination_table = "supervision_level_log"


@case(tags="lookups")
def case_supervision_log_lookups(test_config):
    lookup_fields = {
        "supervisionlevel": {"Ord Risk Lvl": "supervision_level_lookup"},
        "assetlevel": {"Ord Risk Lvl": "asset_level_lookup"},
    }
    merge_columns = {"source": "Order No", "transformed": "c_order_no"}

    config = test_config

    source_columns = list(set([f'"{y}"' for x in lookup_fields.values() for y in x]))
    transformed_columns = [f'"{x}"' for x in lookup_fields.keys()]

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

    return (lookup_fields, merge_columns, source_query, transformed_query, module_name)


@case(tags="calculated")
def case_supervision_log_calcs(test_config):

    today = pd.Timestamp(2021, 1, 6)
    calculated_fields = {
        "appliesfrom": today,
        "createddate": today,
    }

    config = test_config
    source_columns = [f'"{x}"' for x in calculated_fields.keys()]

    source_query = f"""
        SELECT
            {', '.join(source_columns)}
        FROM {config.etl2_schema}.{destination_table}
    """

    return (calculated_fields, source_query, module_name)


@case(tags="one_to_one_joins")
def case_supervision_level_join(test_config):
    join_columns = {
        "order_id": {"cases": "id"},
    }
    merge_columns = {"fk_child": "c_order_no", "fk_parent": "c_order_no"}

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
def case_supervision_level_count(test_config):

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
