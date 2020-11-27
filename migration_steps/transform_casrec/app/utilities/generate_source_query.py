import sys
import os
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import logging
import helpers

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


def format_additional_col_alias(original_column_name: str) -> str:
    return f"c_{original_column_name.lower().replace(' ', '_')}"


def additional_cols(additional_columns: list) -> list:
    return [
        {"casrec_column_name": x, "alias": format_additional_col_alias(x)}
        for x in additional_columns
    ]


def generate_select_string_from_mapping(
    mapping: dict, source_table_name: str, db_schema: str, additional_columns: list = []
) -> str:

    cols = []
    for destination_column, source_details in mapping.items():
        if (
            source_details["casrec_table"].lower() == source_table_name
            and source_details["casrec_column_name"] != ""
        ):
            alias = (
                source_details["alias"]
                if "alias" in source_details
                else source_details["casrec_column_name"]
            )
            col_name = source_details["casrec_column_name"]
            cols.append({"casrec_column_name": col_name, "alias": alias})

    additional_columns_list = additional_cols(additional_columns)

    log.log(
        config.VERBOSE,
        f"columns from mapping: " f"{[x['casrec_column_name'] for x in cols]}",
    )
    log.log(
        config.VERBOSE,
        f"additional columns: "
        f"{[x['casrec_column_name'] for x in additional_columns_list]}",
    )

    col_names_with_alias = cols + additional_columns_list

    statement = "SELECT "

    for i, col in enumerate(col_names_with_alias):
        if isinstance(col["casrec_column_name"], list):

            for j, c in enumerate(col["casrec_column_name"]):
                statement += f'"{c}" as "{c}"'
                if j + 1 < len(col["casrec_column_name"]):
                    statement += ", "

        else:
            statement += f"\"{col['casrec_column_name']}\" as \"{col['alias']}\""

        if i + 1 < len(col_names_with_alias):
            statement += ", "

        else:
            statement += " "

    statement += f"FROM {db_schema}.{source_table_name};"

    log.debug(f"Using SQL statement to select from source database:\n{statement}")

    return statement
