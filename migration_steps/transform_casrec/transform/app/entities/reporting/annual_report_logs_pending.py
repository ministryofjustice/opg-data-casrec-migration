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
from utilities.standard_transformations import calculate_duedate

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
                0 AS numberofchaseletters,
                "Case" AS c_case
            FROM {db_config["source_schema"]}.pat
            WHERE "Report Due" != ''
            LIMIT {chunk_size} OFFSET {offset}
        """

        annual_report_log_df = pd.read_sql_query(
            sql=chunk_query, con=db_config["db_connection_string"]
        )

        """
        TODO
        set reportingperiodstartdate:
        1. Get latest reporting period for the client and store the end date
        2. Add 1 day to this end date and use value to set reportingperiodstartdate
        """

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

        # calculate the duedate
        annual_report_log_df = calculate_duedate(
            original_col="reportingperiodenddate",
            result_col="duedate",
            df=annual_report_log_df,
        )

        # order_id is NULL for now
        annual_report_log_df["order_id"] = None

        annual_report_log_df = reapply_datatypes_to_fk_cols(
            columns=["client_id", "order_id"], df=annual_report_log_df
        )

        # set an ID on all the new records
        annual_report_log_df = add_unique_id(
            db_conn_string=db_config["db_connection_string"],
            db_schema=db_config["target_schema"],
            table_definition=table_definition,
            source_data_df=annual_report_log_df,
        )

        target_db.insert_data(
            table_name=table_definition["destination_table_name"],
            df=annual_report_log_df,
            sirius_details=sirius_details,
        )

        log.info(
            f"Inserted {num_rows} records into {table_definition['destination_table_name']} (pending) table"
        )
