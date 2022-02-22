from custom_errors import EmptyDataFrame
from utilities.basic_data_table import get_basic_data_table
import logging
import os
import pandas as pd

from helpers import get_mapping_dict, get_table_def
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from transform_data.unique_id import add_unique_id

log = logging.getLogger("root")


def insert_annual_report_type_assignments(db_config, target_db, mapping_file):
    table_definition = get_table_def(mapping_name=mapping_file)

    sirius_details = get_mapping_dict(
        file_name=f"{mapping_file}_mapping",
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1

    table_created = False
    target_schema = db_config["target_schema"]

    # How many rows in annual_report_logs table?
    # Once offset >= this count, stop querying.
    report_logs_count_df = pd.read_sql_query(
        f"SELECT COUNT(id) AS num_reports FROM {target_schema}.annual_report_logs",
        db_config["db_connection_string"],
    )
    num_reports = int(report_logs_count_df.head(1)["num_reports"].values[0])

    while offset < num_reports:
        # Each "PENDING" annual report log gets a single report type assignment;
        # I originally did this in pandas then thought I'll do it in SQL, so I can
        # simultaneously wipe out the need for validation SQL
        report_logs_query = f"""
            SELECT
                pending_reports.*,
                (CASE
                    WHEN pending_reports.reporttype IN ('OPG102', 'OPG103') THEN 'pfa'
                    ELSE '-'
                END) AS type
            FROM (
                SELECT
                    reports.annualreport_id,
                    (CASE
                        WHEN
                            reports.orderstatus = 'ACTIVE' AND sll.supervisionlevel = 'GENERAL'
                        THEN
                            CASE
                                WHEN sll.assetlevel IN ('HIGH', 'UNKNOWN') THEN 'OPG102'
                                WHEN sll.assetlevel = 'LOW' THEN 'OPG103'
                                ELSE NULL
                            END
                        ELSE
                            NULL
                    END) AS reporttype
                FROM (
                    SELECT arl.id AS annualreport_id,
                    c.id AS order_id,
                    c.orderstatus AS orderstatus,
                    row_number() OVER (
                        PARTITION BY arl.c_case
                        ORDER BY arl.reportingperiodenddate DESC
                    ) AS rownum
                    FROM {target_schema}.annual_report_logs arl
                    INNER JOIN {target_schema}.persons p
                    ON arl.client_id = p.id
                    INNER JOIN {target_schema}.cases c
                    ON p.caserecnumber = c.caserecnumber
                    WHERE arl.status = 'PENDING'
                    AND c.type = 'order'
                    OFFSET {offset} LIMIT {chunk_size}
                ) AS reports
                INNER JOIN {target_schema}.supervision_level_log sll
                ON reports.order_id = sll.order_id
                WHERE reports.rownum = 1
            ) AS pending_reports
        """

        report_logs_df = pd.read_sql_query(
            report_logs_query, db_config["db_connection_string"]
        )

        if len(report_logs_df) == 0:
            # If we haven't inserted any records yet, table wouldn't have been created,
            # so attempt to create it here. NB we are likely to never reach this code,
            # as we will have at least one record in annual_report_logs which triggers
            # insert_data().
            if not table_created:
                target_db.create_empty_table(
                    sirius_details=sirius_details, df=report_logs_df
                )
        else:
            # Add an id column (because we haven't used the get_basic_data_table() function,
            # we have to do it manually)
            report_logs_df = add_unique_id(
                db_conn_string=db_config["db_connection_string"],
                db_schema=db_config["target_schema"],
                table_definition=table_definition,
                source_data_df=report_logs_df,
            )

            target_db.insert_data(
                table_name=table_definition["destination_table_name"],
                df=report_logs_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

        # Table will either have been created with create_empty_table()
        # because the dataframe was empty, or implicitly created by insert_data()
        table_created = True

        offset += chunk_size
        chunk_no += 1
