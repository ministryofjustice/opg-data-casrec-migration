import pandas as pd

from custom_errors import EmptyDataFrame
from utilities.basic_data_table import get_basic_data_table


def do_finance_ledger_credits_prep(db_config, target_db, mapping_file_name):
    invoice_query = f'select reference as invoice_ref from {db_config["target_schema"]}.finance_invoice;'

    return {
        'invoice_df': pd.read_sql_query(invoice_query, db_config["db_connection_string"])
    }

def get_finance_ledger_credits_chunk(
    db_config,
    mapping_file_name,
    table_definition,
    sirius_details,
    chunk_size,
    offset,
    prep
):
    try:
        credits_df = get_basic_data_table(
            db_config=db_config,
            mapping_file_name=mapping_file_name,
            table_definition=table_definition,
            sirius_details=sirius_details,
            chunk_details={"chunk_size": chunk_size, "offset": offset},
        )
    except EmptyDataFrame as e:
        more_records = (e.empty_data_frame_type != 'chunk')
        return (e.df, more_records)

    invoice_df = prep['invoice_df']

    credits_joined_df = credits_df.merge(
        invoice_df,
        how="inner",
        left_on="c_orig_invoice",
        right_on="invoice_ref",
    )

    return (credits_joined_df, True)
