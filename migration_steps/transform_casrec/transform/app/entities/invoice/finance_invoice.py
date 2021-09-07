import pandas as pd
from custom_errors import EmptyDataFrame

from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table
import logging
import os

from helpers import get_mapping_dict, get_table_def

log = logging.getLogger("root")


def insert_finance_invoice(target_db, db_config, mapping_file):

    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1

    persons_query = (
        f'select "id", "caserecnumber" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_client';"
    )
    persons_df = pd.read_sql_query(persons_query, db_config["db_connection_string"])
    persons_df = persons_df[["id", "caserecnumber"]]

    feecheck_query = f'select "Invoice Number", "GL Date" from {db_config["source_schema"]}.sop_feecheck;'
    feecheck_df = pd.read_sql_query(feecheck_query, db_config["db_connection_string"])
    feecheck_df = feecheck_df[["Invoice Number", "GL Date"]]

    mapping_file_name = f"{mapping_file}_mapping"
    table_definition = get_table_def(mapping_name=mapping_file)
    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )
    while True:
        try:
            invoice_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

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

            target_db.insert_data(
                table_name=table_definition["destination_table_name"],
                df=invoice_joined_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

            offset += chunk_size
            chunk_no += 1

        except EmptyDataFrame:

            target_db.create_empty_table(sirius_details=sirius_details)

            break

        except Exception as e:
            log.error(f"Unexpected error: {e}")
            os._exit(1)