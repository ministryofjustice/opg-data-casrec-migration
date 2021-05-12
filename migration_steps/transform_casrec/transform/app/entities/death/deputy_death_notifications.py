import logging

import pandas as pd
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table

log = logging.getLogger("root")
definition = {
    "source_table_name": "deputy",
    "source_table_additional_columns": ["Stat", "Deputy No"],
    "source_not_null_cols": ["Disch Death"],
    "destination_table_name": "death_notifications",
}

mapping_file_name = "deputy_death_notifications_mapping"


def insert_deputy_death_notifications(db_config, target_db):

    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1

    persons_query = (
        f'select "id", "c_deputy_no" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_deputy';"
    )
    persons_df = pd.read_sql_query(persons_query, db_config["db_connection_string"])

    persons_df = persons_df[["id", "c_deputy_no"]]

    while True:
        try:
            sirius_details, deputy_death_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=definition,
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
                table_name=definition["destination_table_name"],
                df=death_joined_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

            offset += chunk_size
            chunk_no += 1

        except Exception:

            log.debug(f"End of insert_deputy_death_notifications")
            break
