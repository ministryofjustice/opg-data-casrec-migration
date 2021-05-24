import numpy as np
import logging

from custom_errors import EmptyDataFrame

import helpers
import os

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


def remove_empty_rows(df, not_null_cols, how="all"):

    if len(not_null_cols) == 0:
        log.debug("No null rows to remove")
        return df

    log.debug(
        f"Removing rows where these fields are all null after transformation: {', '.join(not_null_cols)}"
    )

    final_df = df
    final_df = final_df.replace("", np.nan)

    cols_to_remove = [x for x in df.columns.tolist() if x in not_null_cols]

    try:
        final_df = final_df.dropna(subset=cols_to_remove, how=how)
    except Exception as e:
        log.debug(f"Problems removing null rows after transformation: {e}")

    log.log(config.VERBOSE, f"Dataframe size after removing empty rows: {len(df)}")

    if len(final_df) == 0:
        raise EmptyDataFrame
    else:
        return final_df
