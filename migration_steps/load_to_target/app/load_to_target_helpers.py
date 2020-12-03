import helpers


def get_cols_from_mapping(
    df, file_name, include_columns=None, exclude_columns=None, reorder_cols=None
):

    sirius_data = helpers.get_mapping_dict(
        file_name=file_name, stage_name="sirius_details", only_complete_fields=True,
    )
    cols_from_mapping = list(sirius_data.keys())

    columns_to_select = [
        x for x in cols_from_mapping if x not in exclude_columns
    ] + include_columns

    if reorder_cols:
        for column_name, position in reorder_cols.items():
            columns_to_select.insert(
                position, columns_to_select.pop(columns_to_select.index(column_name))
            )

    df = df[columns_to_select]

    return df
