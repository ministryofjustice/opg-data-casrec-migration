import pandas as pd
from utilities.basic_data_table import get_basic_data_table

from custom_errors import EmptyDataFrame
from helpers import get_mapping_dict, get_table_def


def insert_cases(db_config, target_db, mapping_file):

    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1

    persons_query = (
        f'select "id", "caserecnumber" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_client';"
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
    while True:
        try:
            cases_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            cases_joined_df = cases_df.merge(
                persons_df,
                how="left",
                left_on="caserecnumber",
                right_on="caserecnumber",
            )

            cases_joined_df["client_id"] = cases_joined_df["id_y"]
            cases_joined_df = cases_joined_df.drop(columns=["id_y"])
            cases_joined_df = cases_joined_df.rename(columns={"id_x": "id"})

            if len(cases_joined_df) > 0:

                target_db.insert_data(
                    table_name=table_definition["destination_table_name"],
                    df=cases_joined_df,
                    sirius_details=sirius_details,
                )

            offset += chunk_size
            chunk_no += 1
        except EmptyDataFrame:

            target_db.create_empty_table(sirius_details=sirius_details)

            break
        except Exception:
            break
