import logging

import pandas as pd

from custom_errors import EmptyDataFrame
from helpers import get_mapping_dict, get_table_def
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table

log = logging.getLogger("root")


def insert_deputy_death_notifications(db_config, target_db, mapping_file):
    chunk_size = db_config["chunk_size"]
    offset = -chunk_size
    chunk_no = 0

    persons_query = (
        f'select "id", "c_deputy_no" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_deputy';"
    )
    persons_df = pd.read_sql_query(persons_query, db_config["db_connection_string"])

    persons_df = persons_df[["id", "c_deputy_no"]]

    mapping_file_name = f"{mapping_file}_mapping"
    table_definition = get_table_def(mapping_name=mapping_file)

    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )
    while True:
        offset += chunk_size
        chunk_no += 1

        try:
            deputy_death_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            death_joined_df = deputy_death_df.merge(
                persons_df, how="left", left_on="c_deputy_no", right_on="c_deputy_no"
            )

            death_joined_df["person_id"] = death_joined_df["id_y"]
            death_joined_df = death_joined_df.drop(columns=["id_y"])
            death_joined_df = death_joined_df.rename(columns={"id_x": "id"})

            death_joined_df = reapply_datatypes_to_fk_cols(
                columns=["person_id"], df=death_joined_df
            )

            target_db.insert_data(
                table_name=table_definition["destination_table_name"],
                df=death_joined_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

        except EmptyDataFrame as empty_data_frame:
            if empty_data_frame.empty_data_frame_type == 'chunk':
                target_db.create_empty_table(sirius_details=sirius_details)
                break
            continue

        except Exception:

            log.debug(f"End of insert_deputy_death_notifications")
            break
