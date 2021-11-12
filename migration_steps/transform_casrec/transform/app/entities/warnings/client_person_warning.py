import logging

import pandas as pd

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


def insert_client_person_warning(db_config, target_db, mapping_file):

    mapping_file_name = f"{mapping_file}_mapping"
    table_definition = get_table_def(mapping_name=mapping_file)
    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    try:

        clients_query = (
            f'select "id", "caserecnumber" from {db_config["target_schema"]}.persons '
            f"where \"type\" = 'actor_client';"
        )
        clients_df = pd.read_sql_query(clients_query, db_config["db_connection_string"])

        client_warning_query = f'select * from {db_config["target_schema"]}.warnings;'
        client_warning_df = pd.read_sql_query(
            client_warning_query, db_config["db_connection_string"]
        )
        if len(client_warning_df) == 0:
            raise EmptyDataFrame

        client_warning_df = client_warning_df[["id", "c_case"]]

        client_warning_df = client_warning_df.merge(
            clients_df,
            how="inner",
            left_on="c_case",
            right_on="caserecnumber",
            suffixes=["_warning", "_client"],
        )

        client_warning_df = client_warning_df.drop(columns=["caserecnumber"])
        client_warning_df = client_warning_df.rename(
            columns={"id_warning": "warning_id", "id_client": "person_id"}
        )
        client_warning_df["casrec_details"] = "{}"

        print(f"len(client_warning_df): {len(client_warning_df)}")

        client_warning_df = reapply_datatypes_to_fk_cols(
            columns=["person_id", "warning_id"], df=client_warning_df
        )
        print(f"len(client_warning_df): {len(client_warning_df)}")

        target_db.insert_data(
            table_name=table_definition["destination_table_name"],
            df=client_warning_df,
            sirius_details=sirius_details,
        )
    except EmptyDataFrame as empty_data_frame:

        target_db.create_empty_table(
            sirius_details=sirius_details, df=empty_data_frame.df
        )

    except Exception as e:
        print(e)
        log.debug(
            "No data to insert",
            extra={
                "file_name": "",
                "error": format_error_message(e=e),
            },
        )
