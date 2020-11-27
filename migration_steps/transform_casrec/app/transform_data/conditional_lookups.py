import logging
import os

import pandas as pd
import helpers

from transform_data.lookup_tables import map_lookup_tables

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


def conditional_lookup(
    column_name: str, original_columns: str, lookup_file_name: str, df: pd.DataFrame
) -> pd.DataFrame:
    log.info("I AM DOING A CONDITIONAL LOOKUP")
    log.log(
        config.DATA, f"conditional\n{df.sample(n=config.row_limit).to_markdown()}",
    )
    conditional_lookup_tables = {column_name: {"lookup_table": lookup_file_name}}

    df = map_lookup_tables(lookup_tables=conditional_lookup_tables, source_data_df=df)

    df[column_name] = df[column_name].apply(lambda x: df[x] if x != "" else "")

    return df
