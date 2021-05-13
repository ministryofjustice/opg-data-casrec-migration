import numpy as np
import logging

log = logging.getLogger("root")


def remove_empty_rows(df, not_null_cols, how="all"):
    final_df = df
    final_df = final_df.replace("", np.nan)

    if len(not_null_cols) > 0:
        final_df = final_df.dropna(subset=not_null_cols, how=how)

    log.debug(f"Rows remaining: {len(final_df)}")

    return final_df
