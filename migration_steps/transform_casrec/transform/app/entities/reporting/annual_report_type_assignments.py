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


# :param group: dataframe containing rows for one combination of
# annualreport_id and caserecnumber
# :returns: reporttype
def _process_orders_for_annual_report_log(group):
    # are there any active orders?
    active_orders = group[group["ord_stat"] == "Active"]

    if len(active_orders) == 0:
        return ""

    # assumption is that we can only have one active order
    active_order = active_orders.iloc[0]

    if active_order["ord_risk_lvl"] == "3":
        return "OPG103"

    return "OPG102"


def calculate_report_types(report_logs_df: pd.DataFrame) -> pd.DataFrame:
    """
    :param report_logs_df: A join between annual_report_logs and the casrec orders
    table on case number. This has one row in it for each annual report log
    + order combination.

    This function groups those rows by annual report ID +
    casrec case number. For each combination, a related set
    of orders from casrec is processed to find any which are
    active and have specific ord risk lvl settings. This is then used to set
    the reporttype as per the criteria in IN-997.

    Note that multiple annual report logs may reference the same case number.
    """
    # Group by annual report ID and casrec case number
    grouped = report_logs_df.groupby(
        ["annualreport_id", "sirius_report_log_casrec_case_no"]
    )

    # Calculate the reporttype field
    report_type_assignments_df = grouped.apply(_process_orders_for_annual_report_log)

    if len(report_type_assignments_df) > 0:
        report_type_assignments_df = report_type_assignments_df.rename(
            "reporttype"
        ).reset_index()

    # Add in a type field set to '-' for all report types
    report_type_assignments_df["type"] = DEFAULT_REPORT_TYPE

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
        try:
            # Each annual report log has a single report type assignment, so start from
            # the annual_report_logs table.
            report_logs_query = f"""
                SELECT arl.id AS annualreport_id,
                arl.c_case AS sirius_report_log_casrec_case_no,
                '{DEFAULT_REPORT_TYPE}' AS type,
                NULL AS reporttype
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

                # Add an id column (because we haven't used the get_basic_data_table() function,
                # we have to do it manually)
                report_type_assignments_df = add_unique_id(
                    db_conn_string=db_config["db_connection_string"],
                    db_schema=db_config["target_schema"],
                    table_definition=table_definition,
                    source_data_df=report_type_assignments_df,
                )

                # Make annualreport_id an Int64 again
                report_type_assignments_df = reapply_datatypes_to_fk_cols(
                    columns=["annualreport_id"], df=report_type_assignments_df
                )

                # Drop columns not required by Sirius
                report_type_assignments_df = report_type_assignments_df.drop(
                    columns=["sirius_report_log_casrec_case_no"]
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
        except Exception as e:
            log.error(f"Unexpected error: {e}")
            log.exception(e)
            os._exit(1)
