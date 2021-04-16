def prep_df_for_merge(df, column):
    df = df.drop_duplicates()

    df = df[df[column].notna()]
    df = df[df[column] != ""]
    df[column] = df[column].astype("float")
    df[column] = df[column].astype("Int32")

    return df
