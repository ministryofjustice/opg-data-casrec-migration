from utilities.generate_source_query import format_additional_col_alias


def source_conditions(df, conditions):

    for column, value in conditions.items():

        if column in df.columns.tolist():
            col_name = column
        else:
            col_name = format_additional_col_alias(original_column_name=column)

        if value == "not null":
            pass
        else:
            df = df.loc[df[col_name] == value]

    return df
