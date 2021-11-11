import datetime as dt


def prep_df_for_merge(df, column):
    df = df.drop_duplicates()

    df = df[df[column].notna()]
    df = df[df[column] != ""]
    df[column] = df[column].astype("float")
    df[column] = df[column].astype("Int32")

    return df


def get_datetime_from_df_row(row, date_col, time_col, default_date=None):
    empty_data = ["", "NaT", "nan"]

    date = (
        row[date_col][0:10] if row[date_col] not in empty_data else default_date
    )

    if date is None:
        return None

    time = (
        row[time_col].split(".")[0]
        if row[time_col] not in empty_data
        else "00:00:00"
    )

    return dt.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
