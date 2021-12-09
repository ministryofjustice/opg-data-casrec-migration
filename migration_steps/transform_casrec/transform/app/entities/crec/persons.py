from custom_errors import EmptyDataFrame
from utilities.basic_data_table import get_basic_data_table
import logging
import os
import pandas as pd

from helpers import get_mapping_dict, get_table_def
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols

log = logging.getLogger("root")


def insert_persons_crec(db_config, target_db, mapping_file):

    persons_query = (
        f'select "id", "caserecnumber", "casrec_details" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_client' order by caserecnumber;"
    )
    persons_df = pd.read_sql_query(persons_query, db_config["db_connection_string"])

    persons_df = persons_df[["id", "caserecnumber"]]

    mapping_file_name = f"{mapping_file}_mapping"
    table_definition = get_table_def(mapping_name=mapping_file)
    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    try:
        crec_df = get_basic_data_table(
            db_config=db_config,
            mapping_file_name=mapping_file_name,
            table_definition=table_definition,
            order_by_cols=["Case"],
            sirius_details=sirius_details,
            chunk_details=None,
        )

        crec_joined_df = crec_df.merge(
            persons_df,
            how="left",
            left_on="c_case",
            right_on="caserecnumber",
            suffixes=["_crec", "_persons"],
        )

        crec_joined_df = crec_joined_df.rename(columns={"id_persons": "id"})

        crec_joined_df = reapply_datatypes_to_fk_cols(columns=["id"], df=crec_joined_df)

        fields_to_update = [
            x
            for x in get_mapping_dict(
                file_name=mapping_file_name,
                stage_name="sirius_details",
                only_complete_fields=False,
                include_pk=False,
                include_fks=False,
            )
        ]

        join_col = "id"

        fields_to_select = fields_to_update + [join_col] + ["casrec_details"]

        crec_joined_df = crec_joined_df[fields_to_select]

        target_db.update_data(
            table_name=table_definition["destination_table_name"],
            df=crec_joined_df,
            fields_to_update=fields_to_update,
            join_column=join_col,
            sirius_details=sirius_details,
        )

    except EmptyDataFrame as empty_data_frame:
        if empty_data_frame.empty_data_frame_type == "chunk":
            target_db.create_empty_table(
                sirius_details=sirius_details, df=empty_data_frame.df
            )
