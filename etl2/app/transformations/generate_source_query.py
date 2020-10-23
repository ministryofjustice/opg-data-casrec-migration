import re


def additional_cols(additional_columns):
    return [
        {"casrec_column_name": x, "alias": f"c_{x.lower().replace(' ', '_')}"}
        for x in additional_columns
    ]


def generate_select_string_from_mapping(
    mapping, source_table_name, additional_columns, db_schema
):

    cols = [
        {"casrec_column_name": v["casrec_column_name"], "alias": v["alias"]}
        for k, v in mapping["simple_mapping"].items()
        if v["casrec_table"].lower() == source_table_name
    ]

    additional_columns_list = additional_cols(additional_columns)

    col_names_with_alias = cols + additional_columns_list

    statement = "SELECT "

    for i, col in enumerate(col_names_with_alias):
        if "," in col["casrec_column_name"]:
            # split comma separated list of cols
            # eg "Dep Adrs1,Dep Adrs2,Dep Adrs3"
            statement += re.sub(
                r"([^,\s][^\,]*[^,\s]*)", r'"\1"', col["casrec_column_name"]
            )

        else:
            statement += f"\"{col['casrec_column_name']}\" as \"{col['alias']}\""

        if i + 1 < len(col_names_with_alias):
            statement += ", "

        else:
            statement += " "

    statement += f"FROM {db_schema}.{source_table_name};"

    return statement
