import pandas as pd

from helpers import get_mapping_dict

from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
import logging

log = logging.getLogger("root")

definition = {
    "destination_table_name": "caseitem_note",
    "source_table_name": "",
    "source_table_additional_columns": [],
}

mapping_file_name = "caseitem_note_mapping"


def insert_caseitem_note(db_config, target_db):

    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1

    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    cases_query = (
        f'select "id", "caserecnumber" from {db_config["target_schema"]}.cases;'
    )
    cases_df = pd.read_sql_query(cases_query, db_config["db_connection_string"])
    log.debug(f"df size - cases_df: {len(cases_df)}")

    while True:

        notes_query = f'select "id", "c_case" from {db_config["target_schema"]}.notes order by "id" limit {chunk_size} offset {offset};'
        notes_df = pd.read_sql_query(notes_query, db_config["db_connection_string"])

        log.debug(f"df size - notes_df: {len(notes_df)}")

        notes_caseitem_df = notes_df.merge(
            cases_df,
            how="left",
            left_on="c_case",
            right_on="caserecnumber",
            suffixes=["_notes", "_case"],
        )

        notes_caseitem_df = notes_caseitem_df.drop(columns=["caserecnumber"])
        notes_caseitem_df = notes_caseitem_df.rename(
            columns={"id_case": "caseitem_id", "id_notes": "note_id"}
        )

        notes_caseitem_df = notes_caseitem_df[notes_caseitem_df["caseitem_id"].notna()]

        notes_caseitem_df = reapply_datatypes_to_fk_cols(
            columns=["note_id", "caseitem_id"], df=notes_caseitem_df
        )

        if len(notes_caseitem_df) > 0:
            log.debug(f"df size - notes_caseitem_df: {len(notes_caseitem_df)}")
            target_db.insert_data(
                table_name=definition["destination_table_name"],
                df=notes_caseitem_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )
        offset += chunk_size
        chunk_no += 1
        if len(notes_caseitem_df) < chunk_size:
            break
