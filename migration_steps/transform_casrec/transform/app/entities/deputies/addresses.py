from custom_errors import EmptyDataFrame
from helpers import get_mapping_dict, get_table_def
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table
import pandas as pd
from transform_data import unique_id as process_unique_id
from utilities.df_helpers import prep_df_for_merge


def insert_addresses_deputies(db_config, target_db, mapping_file):

    deputyship_query = f"""
        select "Dep Addr No", "Deputy No"
        from {db_config['source_schema']}.deputyship
    """
    deputyship_df = pd.read_sql_query(
        deputyship_query, db_config["db_connection_string"]
    )

    deputyship_df = prep_df_for_merge(df=deputyship_df, column="Dep Addr No")

    deputy_persons_query = f"""
        select c_deputy_no, id as person_id
        from {db_config['target_schema']}.persons
        where casrec_mapping_file_name = 'deputy_persons_mapping'
    """

    deputy_persons_df = pd.read_sql_query(
        deputy_persons_query, db_config["db_connection_string"]
    )

    chunk_size = db_config["chunk_size"]
    offset = -chunk_size
    chunk_no = 0

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
            addresses_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            addresses_df = prep_df_for_merge(df=addresses_df, column="c_dep_addr_no")

            address_deputyship_joined_df = addresses_df.merge(
                deputyship_df,
                how="left",
                left_on="c_dep_addr_no",
                right_on="Dep Addr No",
            )

            address_persons_joined_df = address_deputyship_joined_df.merge(
                deputy_persons_df,
                how="left",
                left_on="Deputy No",
                right_on="c_deputy_no",
            )

            address_persons_joined_df = address_persons_joined_df.drop(
                columns=["Dep Addr No", "Deputy No"]
            )

            address_persons_joined_df["person_id"] = (
                address_persons_joined_df["person_id"]
                .fillna(0)
                .astype(int)
                .astype(object)
                .where(address_persons_joined_df["person_id"].notnull())
            )

            address_persons_joined_df = address_persons_joined_df.drop_duplicates()

            address_persons_joined_df = address_persons_joined_df.drop(columns=["id"])

            address_persons_joined_df = process_unique_id.add_unique_id(
                db_conn_string=db_config["db_connection_string"],
                db_schema=db_config["target_schema"],
                table_definition=table_definition,
                source_data_df=address_persons_joined_df,
            )

            # some addresses don't seem to match up with people...
            address_persons_joined_df = address_persons_joined_df[
                address_persons_joined_df["person_id"].notna()
            ]

            address_persons_joined_df = reapply_datatypes_to_fk_cols(
                columns=["person_id"], df=address_persons_joined_df
            )

            target_db.insert_data(
                table_name=table_definition["destination_table_name"],
                df=address_persons_joined_df,
                sirius_details=sirius_details,
                chunk_no=chunk_no,
            )

        except EmptyDataFrame as empty_data_frame:
            if empty_data_frame.empty_data_frame_type == "chunk":
                target_db.create_empty_table(
                    sirius_details=sirius_details, df=empty_data_frame.df
                )
                break
            continue
