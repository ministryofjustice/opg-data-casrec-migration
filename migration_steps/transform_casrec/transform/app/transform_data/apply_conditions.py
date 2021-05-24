from utilities.generate_source_query import format_additional_col_alias

import logging
import os
import numpy as np

import helpers
from custom_errors import EmptyDataFrame

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


def source_conditions(df, conditions):
    df_cols = {k: v for k, v in conditions.items() if k in df.columns.tolist()}
    additional_cols = {
        format_additional_col_alias(original_column_name=k): v
        for k, v in conditions.items()
        if k not in df.columns.tolist()
    }
    renamed_conditions = {**df_cols, **additional_cols}

    not_null_cols = [k for k, v in conditions.items() if v == "not null"]

    df = remove_empty_rows(df, not_null_cols)

    for column, value in renamed_conditions.items():
        if column not in not_null_cols:
            df = df.loc[df[column] == value]

    log.log(config.VERBOSE, f"Dataframe size after applying conditions: {len(df)}")

    return df


def remove_empty_rows(df, not_null_cols, how="all"):

    if len(not_null_cols) == 0:
        log.debug("No null rows to remove")
        return df

    log.debug(
        f"Removing rows where these fields are all null: {', '.join(not_null_cols)}"
    )

    final_df = df
    final_df = final_df.replace("", np.nan)
    final_df = final_df.replace(" ", np.nan)
    final_df = final_df.replace("0", np.nan)

    cols_to_remove = [x for x in df.columns.tolist() if x in not_null_cols]

    try:
        final_df = final_df.dropna(subset=cols_to_remove, how=how)
    except Exception as e:
        log.debug(f"Problems removing null rows: {e}")

    log.log(config.VERBOSE, f"Dataframe size after removing empty rows: {len(df)}")

    if len(final_df) == 0:
        raise EmptyDataFrame
    else:
        return final_df
