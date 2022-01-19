from custom_errors import EmptyDataFrame
from utilities.basic_data_table import get_basic_data_table
import logging
import os
import pandas as pd

from helpers import get_mapping_dict, get_table_def
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from transform_data.unique_id import add_unique_id

log = logging.getLogger("root")


# Until we work out what to do with the type column
DEFAULT_REPORT_TYPE = "-"


# :param row: single row with ord_stat and ord_risk_lvl columns;
#      this will be the row from the orders for this annual report log
#      with the latest date
# :returns: reporttype value, or None if no mapping exists
def _calculate_reporttype(row):
    ord_risk_lvl = row["ord_risk_lvl"]

    if ord_risk_lvl == "3":
        return "OPG103"

    if ord_risk_lvl in ["1", "2", "2A"]:
        return "OPG102"

    return None


def calculate_report_types(report_logs_df: pd.DataFrame) -> pd.DataFrame:
    """
    :param report_logs_df: A join between annual_report_logs and the casrec orders
    table on case number. This has one row in it for each annual report log
    + order combination.

    This function groups those rows by annual report ID + end date +
    casrec case number. Only the combination with the latest end date has
    its reporttype set. This is done by considering the related set
    of orders from casrec to find any which are Active and have specific
    ord risk lvl settings, as per the criteria in IN-997.
    """
    report_type_assignments_df = pd.DataFrame()

    # So we can use idxmax() to get the latest date
    report_logs_df["end_date"] = pd.to_datetime(
        report_logs_df["end_date"], format="%Y-%m-%d"
    )

    # Group by annual report ID and casrec case number
    grouped = report_logs_df.groupby(
        ["annualreport_id", "sirius_report_log_casrec_case_no"]
    )

    # Select the order row with the latest end date from each group
    # and determine its reporttype
    for _, group in grouped:
        with_active_orders = group[group["ord_stat"] == "Active"]

        if len(with_active_orders) > 0:
            # Use the latest "Active" order to determine reporttype
            latest_row = with_active_orders.loc[
                with_active_orders["end_date"].idxmax()
            ].copy()
            latest_row["reporttype"] = _calculate_reporttype(latest_row)
        else:
            # No active order; use the latest "Closed" row and
            # set reporttype to null
            latest_row = group.loc[group["end_date"].idxmax()].copy()
            latest_row["reporttype"] = None

        report_type_assignments_df = report_type_assignments_df.append(latest_row)

    # Cast annualreport_id to correct datatype
    report_type_assignments_df["annualreport_id"] = report_type_assignments_df[
        "annualreport_id"
    ].astype("int64")

    # Drop columns not required by Sirius
    report_type_assignments_df = report_type_assignments_df.drop(
        columns=[
            "end_date",
            "sirius_report_log_casrec_case_no",
            "ord_stat",
            "ord_risk_lvl",
        ]
    )

    report_type_assignments_df.reset_index(inplace=True, drop=True)

    return report_type_assignments_df


def insert_annual_report_type_assignments(db_config, target_db, mapping_file):
    table_definition = get_table_def(mapping_name=mapping_file)

    sirius_details = get_mapping_dict(
        file_name=f"{mapping_file}_mapping",
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    orders_query = f"""
        SELECT ord."Ord Stat" AS ord_stat, ord."Ord Risk Lvl" AS ord_risk_lvl,
        ord."Case" AS casrec_order_case_no
        FROM {db_config["source_schema"]}.order ord
    """

    orders_df = pd.read_sql_query(orders_query, db_config["db_connection_string"])

    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1

    table_created = False
    has_more_records = True

    while has_more_records:
        # Each annual report log has a single report type assignment, so start from
        # the annual_report_logs table.
        report_logs_query = f"""
            SELECT arl.id AS annualreport_id,
            arl.reportingperiodenddate as end_date,
            arl.c_case AS sirius_report_log_casrec_case_no
            FROM {db_config["target_schema"]}.annual_report_logs arl
            OFFSET {offset} LIMIT {chunk_size}
        """

        report_logs_df = pd.read_sql_query(
            report_logs_query, db_config["db_connection_string"]
        )

        # Dataframe is unfiltered, so if it has no records,
        # we have reached the end of the annual_report_logs table
        if len(report_logs_df) == 0:
            has_more_records = False

            # If we haven't inserted any records yet, table wouldn't have been created,
            # so attempt to create it here. NB we are likely to never reach this code,
            # as we will have at least one record in annual_report_logs which triggers
            # insert_data().
            if not table_created:
                target_db.create_empty_table(
                    sirius_details=sirius_details, df=report_logs_df
                )
        else:
            # Join to orders; this is so we can query across Ord Stat and Ord Risk Lvl
            # on orders associated with each annual report log. This is a left join
            # as there may potentially be no orders for a report log.
            report_logs_df = report_logs_df.merge(
                orders_df,
                how="left",
                left_on="sirius_report_log_casrec_case_no",
                right_on="casrec_order_case_no",
            )

            report_type_assignments_df = calculate_report_types(report_logs_df)

            # Add a default type column until we work out what this should contain
            report_type_assignments_df["type"] = DEFAULT_REPORT_TYPE

            # Add an id column (because we haven't used the get_basic_data_table() function,
            # we have to do it manually)
            report_type_assignments_df = add_unique_id(
                db_conn_string=db_config["db_connection_string"],
                db_schema=db_config["target_schema"],
                table_definition=table_definition,
                source_data_df=report_type_assignments_df,
            )

            target_db.insert_data(
                table_name=table_definition["destination_table_name"],
                df=report_type_assignments_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

        # Table will either have been created with create_empty_table()
        # because the dataframe was empty, or implicitly created by insert_data()
        table_created = True

        offset += chunk_size
        chunk_no += 1
