from custom_errors import EmptyDataFrame
from helpers import get_mapping_dict, get_table_def
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table
import pandas as pd
from transform_data import unique_id as process_unique_id
from utilities.df_helpers import prep_df_for_merge


def insert_addresses_deputies(db_config, target_db, mapping_file):
    casrec_schema = db_config["source_schema"]
    target_schema = db_config["target_schema"]
    pro_dep_types = ("20", "21", "22", "24", "25", "26", "27", "28", "29", "63", "71")

    # All the rows in deplink which relate to PRO deputies but are not the main address,
    # combined with all rows from deputy_address whose Dep Addr No is not in deplink
    # (i.e. Lay and PA deputies)
    deplink_query = f"""
        SELECT DISTINCT person_id, "Dep Addr No" FROM (
            select p.id as person_id, dl."Dep Addr No"
            from {casrec_schema}.deplink dl
            inner join {casrec_schema}.deputy d on d."Deputy No" = dl."Deputy No"
            inner join {target_schema}.persons p on CAST(p.deputynumber AS INT) = CAST(d."Deputy No" AS INT)
            WHERE dl."Main Addr" = '1'
            AND d."Dep Type" IN {pro_dep_types}

            UNION

            SELECT p.id AS person_id, ds."Dep Addr No"
            FROM {casrec_schema}.deputy d
            INNER JOIN {target_schema}.persons p
            ON CAST(d."Deputy No" AS INT) = CAST(p.deputynumber AS INT)
            INNER JOIN {casrec_schema}.deputyship ds
            ON d."Deputy No" = ds."Deputy No"
            WHERE d."Dep Type" NOT IN {pro_dep_types}
        ) da
    """
    deplink_df = pd.read_sql_query(deplink_query, db_config["db_connection_string"])

    deplink_df = prep_df_for_merge(df=deplink_df, column="Dep Addr No")

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

            address_persons_joined_df = addresses_df.merge(
                deplink_df,
                how="inner",
                left_on=["c_dep_addr_no"],
                right_on=["Dep Addr No"],
            )

            address_persons_joined_df = address_persons_joined_df.drop(
                columns=["Dep Addr No", "id"]
            )

            address_persons_joined_df["person_id"] = (
                address_persons_joined_df["person_id"].astype(int).astype(object)
            )

            address_persons_joined_df = address_persons_joined_df.drop_duplicates()

            address_persons_joined_df = process_unique_id.add_unique_id(
                db_conn_string=db_config["db_connection_string"],
                db_schema=db_config["target_schema"],
                table_definition=table_definition,
                source_data_df=address_persons_joined_df,
            )

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
