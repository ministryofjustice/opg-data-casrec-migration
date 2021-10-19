import numpy as np
import pandas as pd

from custom_errors import EmptyDataFrame
from utilities.basic_data_table import get_basic_data_table


def do_finance_allocation_credits_prep(db_config, target_db, mapping_file_name):
    feecheck_query = f'''
        select "Invoice Number", "GL Date" as allocateddate, \'ALLOCATED\' as status
        from {db_config["source_schema"]}.sop_feecheckcredits;
    '''

    ledger_query = f'''
        select id as ledger_entry_id, c_invoice_no as ledger_ref
        from {db_config["target_schema"]}.finance_ledger;
    '''

    invoice_query = f'''
        select id as invoice_id, reference as invoice_ref from {db_config["target_schema"]}.finance_invoice;
    '''

    return {
        'feecheck_df': pd.read_sql_query(feecheck_query, db_config["db_connection_string"]),
        'ledger_df': pd.read_sql_query(ledger_query, db_config["db_connection_string"]),
        'invoice_df': pd.read_sql_query(invoice_query, db_config["db_connection_string"])
    }

def get_finance_allocation_credits_chunk(
    db_config,
    mapping_file_name,
    table_definition,
    sirius_details,
    chunk_size,
    offset,
    prep
):
    try:
        credits_allocations_df = get_basic_data_table(
            db_config=db_config,
            mapping_file_name=mapping_file_name,
            table_definition=table_definition,
            sirius_details=sirius_details,
            chunk_details={"chunk_size": chunk_size, "offset": offset},
        )
    except EmptyDataFrame as e:
        more_records = (e.empty_data_frame_type != 'chunk')
        return (e.df, more_records)

    credits_allocations_df = credits_allocations_df.merge(
        prep['invoice_df'],
        how="inner",
        left_on="c_orig_invoice",
        right_on="invoice_ref",
    )

    credits_allocations_df = credits_allocations_df.merge(
        prep['ledger_df'],
        how="left",
        left_on="c_invoice_no",
        right_on="ledger_ref",
    )

    credits_allocations_df = credits_allocations_df.merge(
        prep['feecheck_df'],
        how="left",
        left_on="c_invoice_no",
        right_on="Invoice Number",
    )

    credits_allocations_df['status'] = credits_allocations_df['status'].fillna('PENDING')

    credits_allocations_df = credits_allocations_df.drop(columns=["ledger_ref", "invoice_ref", "Invoice Number"])

    credits_allocations_df.allocateddate.fillna(value=np.nan, inplace=True)

    return (credits_allocations_df, True)
