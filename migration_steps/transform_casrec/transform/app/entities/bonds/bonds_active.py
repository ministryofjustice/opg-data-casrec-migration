from custom_errors import EmptyDataFrame
from helpers import get_mapping_dict, get_table_def
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table
import pandas as pd


def insert_bonds_active(target_db, db_config, mapping_file):
    chunk_size = db_config["chunk_size"]
    offset = -chunk_size
    chunk_no = 0

    existing_cases_query = f"""
        SELECT c_cop_case, c_bond_no, id from {db_config['target_schema']}.cases;
    """

    existing_cases_df = pd.read_sql_query(
        existing_cases_query, db_config["db_connection_string"]
    )

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
            bonds_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            bonds_cases_joined_df = bonds_df.merge(
                existing_cases_df,
                how="left",
                left_on="c_cop_case",
                right_on="c_cop_case",
            )

            bonds_cases_joined_df = bonds_cases_joined_df.rename(
                columns={"id_x": "id", "id_y": "order_id"}
            )

            bonds_cases_joined_df = reapply_datatypes_to_fk_cols(
                columns=["order_id"], df=bonds_cases_joined_df
            )

            target_db.insert_data(
                table_name=table_definition["destination_table_name"],
                df=bonds_cases_joined_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

        except EmptyDataFrame as empty_data_frame:
            if empty_data_frame.empty_data_frame_type == 'chunk':
                target_db.create_empty_table(sirius_details=sirius_details, df=empty_data_frame.df)
                break
            continue

        except Exception:
            break
