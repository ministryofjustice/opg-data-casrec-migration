from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table
import pandas as pd

definition = {
    "source_table_name": "order",
    "source_table_additional_columns": ["CoP Case"],
    "source_conditions": {"Bond No.": "not null"},
    "destination_table_name": "bonds",
}

mapping_file_name = "bonds_mapping"


def insert_bonds(target_db, db_config):
    chunk_size = db_config["chunk_size"]
    offset = 0
    chunk_no = 1

    existing_cases_query = f"""
        SELECT c_cop_case, c_bond_no, id from {db_config['target_schema']}.cases;
    """

    existing_cases_df = pd.read_sql_query(
        existing_cases_query, db_config["db_connection_string"]
    )
    existing_cases_df = existing_cases_df.loc[existing_cases_df["c_bond_no"].notnull()]

    while True:
        try:
            sirius_details, bonds_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=definition,
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
            # bonds_cases_joined_df = bonds_cases_joined_df.loc[
            #     bonds_cases_joined_df["bondreferencenumber"] != ""
            # ]

            target_db.insert_data(
                table_name=definition["destination_table_name"],
                df=bonds_cases_joined_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

            offset += chunk_size
            chunk_no += 1
        except Exception:
            break
