from datetime import datetime

from pytest_cases import case


module_name = "supervision_level_log"
source_table = "order"
destination_table = "supervision_level_log"


@case(tags="lookups")
def case_supervision_log_lookups(test_config):
    lookup_fields = {
        "supervisionlevel": {"Ord Risk Lvl": "supervision_level_lookup"},
        "assetlevel": {"Ord Risk Lvl": "asset_level_lookup"},
    }
    merge_columns = {"source": "Case", "transformed": "c_case"}

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

    today = datetime.today().strftime("%Y-%m-%d")

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
