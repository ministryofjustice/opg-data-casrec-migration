from custom_errors import EmptyDataFrame
from utilities.basic_data_table import get_basic_data_table
import logging
import os
import pandas as pd

from helpers import get_mapping_dict
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols

log = logging.getLogger("root")

definition = {
    "source_table_name": "crec",
    "source_table_additional_columns": ["Modify", "at.1", "Case"],
    "source_conditions": {
        "convert_to_timestamp": {"date": "Modify", "time": "at.1"},
        "latest": {"col": "timestamp", "per": "Case"},
    },
    "destination_table_name": "persons",
}


def insert_persons_crec(db_config, target_db, mapping_file):

    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1

    persons_query = (
        f'select "id", "caserecnumber", "casrec_details" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_client';"
    )
    persons_df = pd.read_sql_query(persons_query, db_config["db_connection_string"])

    persons_df = persons_df[["id", "caserecnumber"]]

    mapping_file_name = f"{mapping_file}_mapping"

    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )
    while True:
        try:
            crec_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            # print(crec_df.sample(10).to_markdown())

            crec_joined_df = crec_df.merge(
                persons_df,
                how="left",
                left_on="c_case",
                right_on="caserecnumber",
                suffixes=["_crec", "_persons"],
            )

            crec_joined_df = crec_joined_df.rename(columns={"id_persons": "id"})

            crec_joined_df = reapply_datatypes_to_fk_cols(
                columns=["id"], df=crec_joined_df
            )

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
                table_name=definition["destination_table_name"],
                df=crec_joined_df,
                fields_to_update=fields_to_update,
                join_column=join_col,
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
