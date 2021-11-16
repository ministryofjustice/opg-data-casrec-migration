import logging
import os

import pandas as pd

import helpers

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


def do_simple_mapping(
    simple_mapping: dict, table_definition: dict, source_data_df: pd.DataFrame
) -> pd.DataFrame:

    source_table_name = table_definition["source_table_name"]

    columns = {}
    for k, v in simple_mapping.items():
        if (
            v["requires_transformation"] == [""]
            and v["casrec_table"].lower() == source_table_name
        ):
            if isinstance(v["alias"], list):
                for a in v["alias"]:
                    columns[a] = k
            else:
                columns[v["alias"]] = k

    result_df = source_data_df.rename(columns=columns)

    log.log(
        config.VERBOSE, f"Dataframe size after simple mappings: {len(source_data_df)}"
    )

    return result_df
