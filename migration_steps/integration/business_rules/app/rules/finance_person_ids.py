import logging
import os
import pandas as pd

from utilities.db_helpers import update_ids
from table_helpers import check_enabled_by_table_name

log = logging.getLogger("root")

environment = os.environ.get("ENVIRONMENT")


def set_finance_person_ids_on_invoices(db_config, target_db_engine):

    if not check_enabled_by_table_name(table_name="finance_invoice"):
        log.info(f"Skip setting finance_person_id on invoices. Invoice entity disabled.")
        return

    invoices_query = (
        f'select "id", "person_id" from {db_config["target_schema"]}.finance_invoice;'
    )
    invoices_df = pd.read_sql_query(invoices_query, target_db_engine)
    invoices_df = invoices_df[["id", "person_id"]]

    finance_person_query = (
        f'select "id" as "finance_person_id", "person_id" from {db_config["sirius_schema"]}.finance_person;'
    )
    finance_person_df = pd.read_sql_query(finance_person_query, db_config["sirius_db_connection_string"])
    finance_person_df = finance_person_df[["finance_person_id", "person_id"]]

    invoices_joined_df = invoices_df.merge(
        finance_person_df,
        how="left",
        left_on="person_id",
        right_on="person_id"
    )

    rows_to_update = zip(invoices_joined_df["id"], invoices_joined_df["finance_person_id"])

    log.debug("Update finance_invoice.finance_person_id....")
    update_ids(
        db_connection_string=db_config["db_connection_string"],
        db_schema=db_config["target_schema"],
        table="finance_invoice",
        column_name="finance_person_id",
        update_data=rows_to_update,
    )
