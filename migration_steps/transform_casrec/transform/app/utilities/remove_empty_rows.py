import numpy as np


def remove_empty_rows(df, required_cols, how="all"):
    final_df = df
    final_df = final_df.replace("", np.nan)
    final_df = final_df.dropna(subset=required_cols, how=how)

    return final_df
