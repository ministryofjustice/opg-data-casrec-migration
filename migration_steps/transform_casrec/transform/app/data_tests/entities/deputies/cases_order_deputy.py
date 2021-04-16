import pandas as pd
import pytest
from pandas.core.common import flatten
from pytest_cases import case


module_name = "order_deputy_mapping"
source_table = "deputy"
destination_table = "order_deputy"


@case(tags="lookups")
def case_order_deputies_lookups(test_config):

    lookup_fields = {
        "statusoncase": {"Stat": "deputy_status_lookup"},
        "relationshiptoclient": {"Dep Type": "deputy_relationship_lookup"},
    }
    merge_columns = {"source": "Deputy No", "transformed": "c_deputy_no"}

    config = test_config

    source_columns = [f'"{y}"' for x in lookup_fields.values() for y in x]
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
        WHERE casrec_mapping_file_name = '{module_name}'
    """

    return (lookup_fields, merge_columns, source_query, transformed_query, module_name)


@case(tags="conditional_lookup")
def case_order_deputies_con_lookups(test_config):

    lookup_fields = {
        "statuschangedate": {
            "cols": {
                "result": "Disch Death",
                "reference": "Stat",
            },
            "lookup_def": "discharge_date_lookup",
        }
    }
    merge_columns = {"source": "Deputy No", "transformed": "c_deputy_no"}

    config = test_config

    source_columns = [
        f'"{x}"'
        for x in flatten(
            [
                list(z.values())
                for x in lookup_fields.values()
                for y, z in x.items()
                if y == "cols"
            ]
        )
    ]
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
        WHERE casrec_mapping_file_name = '{module_name}'
    """

    return (lookup_fields, merge_columns, source_query, transformed_query, module_name)


#  is this even possible?
#
# @case(tags="row_count")
# def case_order_deputies_count(test_config):
#
#     config = test_config
#     source_query = f"""
#         SELECT
#             *
#         FROM {config.schemas['pre_transform']}.{source_table}
#     """
#
#     transformed_query = f"""
#         SELECT
#             *
#         FROM {config.schemas['post_transform']}.{destination_table}
#         WHERE casrec_mapping_file_name = '{module_name}'
#     """
#
#     return (source_query, transformed_query, module_name)
