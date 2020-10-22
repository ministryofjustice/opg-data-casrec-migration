import re


mapping = {
    "simple_mapping": {
        "orderdate": {
            "casrec_table": "ORDER",
            "casrec_column_name": "Made Date",
            "alias": "Made Date",
        },
        "orderissuedate": {
            "casrec_table": "ORDER",
            "casrec_column_name": "Issue Date",
            "alias": "Issue Date",
        },
        "orderexpirydate": {
            "casrec_table": "ORDER",
            "casrec_column_name": "Made Date",
            "alias": "Made Date 1",
        },
        "statusdate": {
            "casrec_table": "ORDER",
            "casrec_column_name": "Made Date",
            "alias": "Made Date 2",
        },
        "caserecnumber": {
            "casrec_table": "ORDER",
            "casrec_column_name": "Case",
            "alias": "Case",
        },
        "ordersubtype": {
            "casrec_table": "ORDER",
            "casrec_column_name": "Ord Type",
            "alias": "Ord Type",
        },
        "casrec_id": {
            "casrec_table": "order",
            "casrec_column_name": "rct",
            "alias": "rct",
        },
    },
    "transformations": {
        "unique_number": [{"original_columns": ["unknown"], "aggregate_col": "uid"}]
    },
    "required_columns": {"type": {"data_type": "str", "default_value": "order"}},
}

source_table_name = "order"
additional_columns = ["Order No"]


def additional_cols(additional_columns):
    return [
        {"casrec_column_name": x, "alias": f"c_{x.lower().replace(' ', '_')}"}
        for x in additional_columns
    ]


def generate_select_string_from_mapping(mapping, source_table_name, db_schema):

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
    statement += f"FROM {db_schema}.{source_table_name} "
    print(statement)
    return f"{statement};"
