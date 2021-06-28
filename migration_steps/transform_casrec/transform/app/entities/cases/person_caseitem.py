import pandas as pd

from custom_errors import EmptyDataFrame
from helpers import get_mapping_dict, format_error_message
import logging

log = logging.getLogger("root")

definition = {
    "destination_table_name": "person_caseitem",
    "source_table_name": "",
    "source_table_additional_columns": [],
}

mapping_file_name = "person_caseitem_mapping"


def insert_person_caseitem(db_config, target_db):

    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    try:
        persons_query = (
            f'select "id", "caserecnumber" from {db_config["target_schema"]}.persons '
            f"where \"type\" = 'actor_client';"
        )
        persons_df = pd.read_sql_query(persons_query, db_config["db_connection_string"])

        cases_query = (
            f'select "id", "caserecnumber" from {db_config["target_schema"]}.cases;'
        )
        cases_df = pd.read_sql_query(cases_query, db_config["db_connection_string"])

        person_caseitem_df = cases_df.merge(
            persons_df,
            how="left",
            left_on="caserecnumber",
            right_on="caserecnumber",
            suffixes=["_case", "_person"],
        )

        person_caseitem_df = person_caseitem_df.drop(columns=["caserecnumber"])
        person_caseitem_df = person_caseitem_df.rename(
            columns={"id_case": "caseitem_id", "id_person": "person_id"}
        )

        person_caseitem_df["casrec_details"] = "{}"

        target_db.insert_data(
            table_name=definition["destination_table_name"],
            df=person_caseitem_df,
            sirius_details=sirius_details,
        )

    except EmptyDataFrame:

        target_db.create_empty_table(sirius_details=sirius_details)

    except Exception as e:
        log.debug(
            "No data to insert",
            extra={
                "file_name": "",
                "error": format_error_message(e=e),
            },
        )
