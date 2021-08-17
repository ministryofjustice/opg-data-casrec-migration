import json
import os
import logging
import sys
from pathlib import Path


current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")


completed_tables = []

log = logging.getLogger("root")

SPECIAL_CASES = ["addresses", "persons"]


def handle_special_cases(table_name, df):
    if table_name == "addresses":
        log.debug("Reformatting 'address_lines' to json")
        df["address_lines"] = df["address_lines"].apply(json.dumps)
    if table_name == "persons":
        log.debug("Reformat 'risk_score' to nullable int")
        df["risk_score"] = df["risk_score"].astype("Int64")
    return df


def replace_with_sql_friendly_chars(row_as_list):
    row = [
        str(
            x.replace("'", "''")
            .replace("NaT", "")
            .replace("<NA>", "")
            .replace("nan", "")
            .replace("None", "")
            .replace("&", "and")
            .replace(";", "-")
            .replace("%", "percent")
        )
        for x in row_as_list
    ]

    return row


def replace_with_sql_friendly_chars_single(val):

    new_val = str(
        val.replace("'", "''")
        .replace("NaT", "")
        .replace("<NA>", "")
        .replace("nan", "")
        .replace("None", "")
        .replace("&", "and")
        .replace(";", "-")
        .replace("%", "percent")
    )

    return new_val


def get_columns_query(table, schema):
    return f"""
        SELECT column_name FROM information_schema.columns
        WHERE table_schema = '{schema}'
        AND table_name = '{table}';
        """


def remove_unecessary_columns(columns, cols_to_keep=[]):
    unecessary_field_names = ["method", "casrec_details"] + cols_to_keep

    return [column for column in columns if column not in unecessary_field_names]
