import pandas as pd
from custom_errors import EmptyDataFrame

from utilities.basic_data_table import get_basic_data_table
import logging
import os

from helpers import get_mapping_dict, get_table_def

log = logging.getLogger("root")


def insert_finance_ledger_credits(target_db, db_config, mapping_file):

    chunk_size = db_config["chunk_size"]
    offset = -chunk_size
    chunk_no = 0

    feecheck_query = f'select "Invoice Number", "GL Date", \'CONFIRMED\' as status from {db_config["source_schema"]}.sop_feecheckcredits;'
    feecheck_df = pd.read_sql_query(feecheck_query, db_config["db_connection_string"])
    feecheck_df = feecheck_df[["Invoice Number", "GL Date", "status"]]

    invoice_query = f'select reference as invoice_ref from {db_config["target_schema"]}.finance_invoice;'
    invoice_df = pd.read_sql_query(invoice_query, db_config["db_connection_string"])
    invoice_df = invoice_df[["invoice_ref"]]

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

        try:
            credits_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            credits_joined_df = credits_df.merge(
                invoice_df,
                how="inner",
                left_on="c_orig_invoice",
                right_on="invoice_ref",
            )

            # Join sop_feecheckcredits (SSCL Credits Transaction Register) so we can populate finance_ledger.confirmeddate
            credits_joined_df = credits_joined_df.merge(
                feecheck_df,
                how="left",
                left_on="c_invoice_no",
                right_on="Invoice Number",
            )
            credits_joined_df = credits_joined_df.rename(
                columns={"GL Date": "confirmeddate"}
            )

            credits_joined_df['status'] = credits_joined_df['status'].fillna('APPROVED')
            credits_joined_df = credits_joined_df.drop(columns=["Invoice Number"])

            target_db.insert_data(
                table_name=table_definition["destination_table_name"],
                df=credits_joined_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

        except EmptyDataFrame as empty_data_frame:
            if empty_data_frame.empty_data_frame_type == 'chunk':
                target_db.create_empty_table(sirius_details=sirius_details)

                break

            continue

        except Exception as e:
            log.error(f"Unexpected error: {e}")
            os._exit(1)
