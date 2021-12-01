import json
import os
import logging
import sys
import re
from pathlib import Path


current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")


completed_tables = []

log = logging.getLogger("root")

SPECIAL_CASES = [
    "addresses",
    "persons",
    "finance_invoice",
    "finance_ledger",
    "finance_remission_exemption",
    "annual_report_logs",
    "annual_report_type_assignments",
]


def handle_special_cases(table_name, df):
    if table_name == "addresses":
        log.debug("Reformatting 'address_lines' to json")
        df["address_lines"] = df["address_lines"].apply(json.dumps)
    if table_name == "persons":
        log.debug("Reformat 'risk_score' to nullable int")
        df["risk_score"] = df["risk_score"].astype("Int64")
        log.debug("Reformat 'feepayer_id' to nullable int")
        df["feepayer_id"] = df["feepayer_id"].astype("Int64")
    if table_name == "finance_invoice":
        log.debug("Reformat 'finance_person_id' to nullable int")
        df["finance_person_id"] = df["finance_person_id"].astype("Int64")
    if table_name == "finance_ledger":
        log.debug("Reformat 'finance_person_id' to nullable int")
        df["finance_person_id"] = df["finance_person_id"].astype("Int64")
    if table_name == "finance_remission_exemption":
        log.debug("Reformat 'finance_person_id' to nullable int")
        df["finance_person_id"] = df["finance_person_id"].astype("Int64")
    if table_name == "annual_report_logs":
        df["client_id"] = df["client_id"].astype("Int64")
        df["order_id"] = df["order_id"].astype("Int64")
    if table_name == "annual_report_type_assignments":
        df["annualreport_id"] = df["annualreport_id"].astype("Int64")
    return df


def get_columns_query(table, schema):
    return f"""
        SELECT column_name FROM information_schema.columns
        WHERE table_schema = '{schema}'
        AND table_name = '{table}';
        """


def remove_unecessary_columns(columns, cols_to_keep=[]):
    unecessary_field_names = ["migration_method", "casrec_details"] + cols_to_keep

    return [column for column in columns if column not in unecessary_field_names]
