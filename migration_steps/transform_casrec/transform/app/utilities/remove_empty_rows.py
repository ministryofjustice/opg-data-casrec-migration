import numpy as np
import logging

from utilities.custom_errors import EmptyDataFrame

log = logging.getLogger("root")


def remove_empty_rows(df, not_null_cols, how="all"):

    final_df = df
    final_df = final_df.replace("", np.nan)

    cols_to_remove = [x for x in df.columns.tolist() if x in not_null_cols]

    if len(cols_to_remove) > 0:
        final_df = final_df.dropna(subset=cols_to_remove, how=how)

    log.debug(f"Rows remaining: {len(final_df)}")

    if len(final_df) == 0:
        raise EmptyDataFrame
    else:
        return final_df
