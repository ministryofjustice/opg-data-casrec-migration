import pandas as pd

from custom_errors import EmptyDataFrame
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table


def do_finance_invoice_prep(db_config, target_db, mapping_file_name):
    persons_query = (
        f'select "id", "caserecnumber" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_client';"
    )
    persons_df = pd.read_sql_query(persons_query, db_config["db_connection_string"])

    feecheck_query = f'select "Invoice Number", "GL Date" from {db_config["source_schema"]}.sop_feecheck;'
    feecheck_df = pd.read_sql_query(feecheck_query, db_config["db_connection_string"])

    return {
        'feecheck_df': feecheck_df,
        'persons_df': persons_df
    }

def get_finance_invoice_chunk(
    db_config,
    mapping_file_name,
    table_definition,
    sirius_details,
    chunk_size,
    offset,
    prep
):
    try:
        invoice_df = get_basic_data_table(
            db_config=db_config,
            mapping_file_name=mapping_file_name,
            table_definition=table_definition,
            sirius_details=sirius_details,
            chunk_details={"chunk_size": chunk_size, "offset": offset},
        )
    except EmptyDataFrame as e:
        more_records = (e.empty_data_frame_type != 'chunk')
        return (e.df, more_records)

    persons_df = prep['persons_df']
    feecheck_df = prep['feecheck_df']

    # Join persons table so we can populate finance_invoice.person_id
    invoice_joined_df = invoice_df.merge(
        persons_df,
        how="left",
        left_on="c_case",
        right_on="caserecnumber",
        suffixes=["_invoices", "_persons"],
    )
    invoice_joined_df = invoice_joined_df.rename(
        columns={"id_persons": "person_id", "id_invoices": "id"}
    )

    # Join sop_feecheck (SSCL Invoice Transaction Register) so we can populate finance_invoice.confirmeddate
    invoice_joined_df = invoice_joined_df.merge(
        feecheck_df,
        how="left",
        left_on="reference",
        right_on="Invoice Number",
    )
    invoice_joined_df = invoice_joined_df.rename(
        columns={"GL Date": "confirmeddate"}
    )
    invoice_joined_df = invoice_joined_df.drop(columns=["Invoice Number"])

    invoice_joined_df = reapply_datatypes_to_fk_cols(
        columns=["person_id"], df=invoice_joined_df
    )

    return (invoice_joined_df, True)
