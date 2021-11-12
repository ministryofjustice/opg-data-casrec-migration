import numpy as np
import pandas as pd
from custom_errors import EmptyDataFrame

from utilities.basic_data_table import get_basic_data_table
import logging
import os

from helpers import get_mapping_dict, get_table_def

log = logging.getLogger("root")


def insert_finance_allocation_credits(target_db, db_config, mapping_file):

    chunk_size = db_config["chunk_size"]
    offset = -chunk_size
    chunk_no = 0

    feecheck_query = f'select "Invoice Number", "GL Date" as allocateddate, \'ALLOCATED\' as status from {db_config["source_schema"]}.sop_feecheckcredits;'
    feecheck_df = pd.read_sql_query(feecheck_query, db_config["db_connection_string"])
    feecheck_df = feecheck_df[["Invoice Number", "allocateddate", "status"]]

    ledger_query = f'''select id as ledger_entry_id,
                        c_invoice_no as ledger_ref
                        from {db_config["target_schema"]}.finance_ledger;'''
    ledger_df = pd.read_sql_query(ledger_query, db_config["db_connection_string"])
    ledger_df = ledger_df[["ledger_entry_id", "ledger_ref"]]

    invoice_query = f'select id as invoice_id, reference as invoice_ref from {db_config["target_schema"]}.finance_invoice;'
    invoice_df = pd.read_sql_query(invoice_query, db_config["db_connection_string"])
    invoice_df = invoice_df[["invoice_id", "invoice_ref"]]

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
            credits_allocations_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            credits_allocations_df = credits_allocations_df.merge(
                invoice_df,
                how="inner",
                left_on="c_orig_invoice",
                right_on="invoice_ref",
            )

            if len(credits_allocations_df) == 0:
                log.debug(f"No data left after inner joining invoices")
                raise EmptyDataFrame(empty_data_frame_type="chunk with conditions applied")

            credits_allocations_df = credits_allocations_df.merge(
                ledger_df,
                how="left",
                left_on="c_invoice_no",
                right_on="ledger_ref",
            )

            credits_allocations_df = credits_allocations_df.merge(
                feecheck_df,
                how="left",
                left_on="c_invoice_no",
                right_on="Invoice Number",
            )

            credits_allocations_df['status'] = credits_allocations_df['status'].fillna('PENDING')

            credits_allocations_df = credits_allocations_df.drop(columns=["ledger_ref", "invoice_ref", "Invoice Number"])

            credits_allocations_df.allocateddate.fillna(value=np.nan, inplace=True)

            target_db.insert_data(
                table_name=table_definition["destination_table_name"],
                df=credits_allocations_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

        except EmptyDataFrame as empty_data_frame:
            if empty_data_frame.empty_data_frame_type == 'chunk':
                target_db.create_empty_table(sirius_details=sirius_details, df=empty_data_frame.df)

                break

            continue

        except Exception as e:
            log.error(f"Unexpected error: {e}")
            os._exit(1)
