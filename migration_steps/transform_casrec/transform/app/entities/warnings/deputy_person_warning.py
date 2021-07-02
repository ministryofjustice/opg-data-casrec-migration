import logging

import pandas as pd
import psycopg2
from psycopg2 import errors

from custom_errors import EmptyDataFrame
from helpers import get_mapping_dict, format_error_message, get_table_def
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols

log = logging.getLogger("root")

# definition = {
#     "destination_table_name": "person_warning",
#     "source_table_name": "",
#     "source_table_additional_columns": [],
# }
#
# mapping_file_name = "person_warning_mapping"


def insert_deputy_person_warning(db_config, target_db, mapping_file):

    mapping_file_name = f"{mapping_file}_mapping"
    table_definition = get_table_def(mapping_name=mapping_file)
    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    try:
        deputys_query = (
            f'select "id", "c_deputy_no" from {db_config["target_schema"]}.persons '
            f"where \"type\" = 'actor_deputy';"
        )
        deputys_df = pd.read_sql_query(deputys_query, db_config["db_connection_string"])

        deputy_warning_query = f"""
                select * from {db_config["target_schema"]}.warnings
                where casrec_mapping_file_name = 'deputy_violent_warnings_mapping';"""
        deputy_warning_df = pd.read_sql_query(
            deputy_warning_query, db_config["db_connection_string"]
        )

        if len(deputy_warning_df) == 0:
            raise EmptyDataFrame

        deputy_warning_df = deputy_warning_df[["id", "c_deputy_no"]]

        deputy_warning_df = deputy_warning_df.merge(
            deputys_df,
            how="left",
            left_on="c_deputy_no",
            right_on="c_deputy_no",
            suffixes=["_warning", "_deputy"],
        )

        deputy_warning_df = deputy_warning_df.rename(
            columns={"id_warning": "warning_id", "id_deputy": "person_id"}
        )
        deputy_warning_df["casrec_details"] = "{}"

        deputy_warning_df = reapply_datatypes_to_fk_cols(
            columns=["person_id", "warning_id"], df=deputy_warning_df
        )

        target_db.insert_data(
            table_name=table_definition["destination_table_name"],
            df=deputy_warning_df,
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
