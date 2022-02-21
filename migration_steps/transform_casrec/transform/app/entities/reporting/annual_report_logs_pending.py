"""
Additional records for annual_report_logs for pending reports,
sourced from casrec pat table.

IMPORTANT: Rather than attempt to create the annual_report_logs
table here, we rely on the function in annual_report_logs.py to
have done that for us by the time this is called. This is because
the table creation function depends on us having a full table
dataframe available to generate the CREATE TABLE SQL. We don't
have that here (as we only have a partial record and no
full mapping from pat -> annual_report_logs), so we can't
rely on the create_empty_table() method to set up the table properly.
"""
from utilities.basic_data_table import get_basic_data_table
import logging
import os
import pandas as pd

from helpers import get_mapping_dict, get_table_def
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from transform_data.unique_id import add_unique_id
from utilities.standard_transformations import (
    calculate_date,
    calculate_duedate,
    calculate_startdate,
)

log = logging.getLogger("root")


def insert_annual_report_logs_pending(db_config, target_db, mapping_file):
    chunk_size = db_config["chunk_size"]
    offset = -chunk_size
    chunk_no = 0

    persons_query = (
        f"select p.id as client_id, p.caserecnumber as caserecnumber "
        f'from {db_config["target_schema"]}.persons as p '
        f"where p.\"type\" = 'actor_client';"
    )

    persons_df = pd.read_sql_query(persons_query, db_config["db_connection_string"])

    # reportingperiodstartdate is the End Date of the most recent
    # reporting period + 1 day; we only consider accounts associated
    # with 'Active' orders
    cases_query = f"""
        SELECT account_case, reportingperiodstartdate
        FROM {db_config["source_schema"]}.order o
        INNER JOIN (
            SELECT
                "Case" as account_case,
                CAST("End Date" AS date) + 1 as reportingperiodstartdate,
                row_number() OVER (
                    PARTITION BY "Case"
                    ORDER BY "End Date" DESC
                ) AS rownum
            FROM {db_config["source_schema"]}.account a
            ORDER BY "Case"
        ) AS cases
        ON o."Case" = cases.account_case
        WHERE cases.rownum = 1
        AND o."Ord Stat" = 'Active';
    """

    cases_df = pd.read_sql_query(cases_query, db_config["db_connection_string"])

    orders_query = f"""
        select order_id, caserecnumber from
        (
            select c.id as order_id, c.caserecnumber,
            row_number() OVER (PARTITION BY a."Case" ORDER BY a."End Date" DESC) as rownum
            from {db_config["target_schema"]}.cases c
            inner join {db_config["source_schema"]}.account a
            on c.caserecnumber = a."Case" and c.orderstatus = 'ACTIVE' and c.type = 'order'
        ) cases
        WHERE rownum = 1
    """

    orders_df = pd.read_sql_query(orders_query, db_config["db_connection_string"])

    mapping_file_name = f"{mapping_file}_mapping"
    table_definition = get_table_def(mapping_name=mapping_file)
    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    while True:
        offset += chunk_size
        chunk_no += 1

        chunk_query = f"""
            SELECT
                "Report Due" AS reportingperiodenddate,
                'PENDING' AS status,
                'NO_REVIEW' AS reviewstatus,
                0 AS numberofchaseletters,
                "Case" AS c_case
            FROM {db_config["source_schema"]}.pat
            WHERE "Report Due" != ''
            LIMIT {chunk_size} OFFSET {offset}
        """

        annual_report_log_df = pd.read_sql_query(
            sql=chunk_query, con=db_config["db_connection_string"]
        )

        num_rows = len(annual_report_log_df)

        # NB we don't try to create the table if there are
        # no records here; see comment at the top of this file for why.
        # Instead, we just exit the loop.
        # Note that we're not doing any filtering or joining on the original
        # dataframe before we check the number of rows, so we can be
        # sure we've reached the end of the pat table at this point.
        if num_rows == 0:
            log.info(f"No data returned from database")
            break

        log.debug(
            f"Found {num_rows} rows in pat table to potentially insert into annual_report_logs"
        )

        # set order_id
        annual_report_log_df = annual_report_log_df.merge(
            orders_df,
            how="left",
            left_on="c_case",
            right_on="caserecnumber",
        )

        # set client_id; inner join used, so if a client doesn't exist
        # for the case attached to the pat record, the report will be removed
        annual_report_log_df = annual_report_log_df.merge(
            persons_df,
            how="inner",
            left_on="c_case",
            right_on="caserecnumber",
        )

        num_rows = len(annual_report_log_df)
        log.debug(f"After joining pat to persons, {num_rows} rows remain")

        if num_rows == 0:
            log.info(
                "No rows remain to insert after join to persons; going to next chunk"
            )
            continue

        # join to set reportingperiodstartdate from the most-recent row in the
        # account table for each pending report
        annual_report_log_df = annual_report_log_df.merge(
            cases_df,
            how="inner",
            left_on="c_case",
            right_on="account_case",
        )

        num_rows = len(annual_report_log_df)
        log.debug(
            f"After joining pat to account (to get most-recent reporting period), "
            f"{num_rows} rows remain"
        )

        if num_rows == 0:
            log.info(
                "No rows remain to insert after join to account; going to next chunk"
            )
            continue

        # calculate the duedate
        annual_report_log_df = calculate_duedate(
            original_col="reportingperiodenddate",
            result_col="duedate",
            df=annual_report_log_df,
        )

        # set an ID on all the new records
        annual_report_log_df = add_unique_id(
            db_conn_string=db_config["db_connection_string"],
            db_schema=db_config["target_schema"],
            table_definition=table_definition,
            source_data_df=annual_report_log_df,
        )

        # set all columns to NULL which aren't set in the dataframe yet;
        # we're doing this manually here because we can't use the get_basic_data_table()
        # to do it for us, because we have a different source table from the one
        # defined in the mapping
        for column in sirius_details.keys():
            if column not in annual_report_log_df:
                annual_report_log_df[column] = None

        annual_report_log_df = reapply_datatypes_to_fk_cols(
            columns=[
                "client_id",
                "order_id",
                "reviewedby_id",
                "lodgingchecklistdocument_id",
            ],
            df=annual_report_log_df,
        )

        # drop columns added when joining to other dataframes
        annual_report_log_df = annual_report_log_df.drop(columns=["account_case"])

        target_db.insert_data(
            table_name=table_definition["destination_table_name"],
            df=annual_report_log_df,
            sirius_details=sirius_details,
        )

        log.info(
            f"Inserted {num_rows} records into {table_definition['destination_table_name']} (pending) table"
        )
