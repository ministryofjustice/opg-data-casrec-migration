from custom_errors import EmptyDataFrame
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table


def get_addresses_clients_chunk(db_config, mapping_file_name, table_definition, sirius_details, chunk_size, offset, prep):
    try:
        addresses_df = get_basic_data_table(
            db_config=db_config,
            mapping_file_name=mapping_file_name,
            table_definition=table_definition,
            sirius_details=sirius_details,
            chunk_details={"chunk_size": chunk_size, "offset": offset},
        )
    except EmptyDataFrame as e:
        more_records = (e.empty_data_frame_type != 'chunk')
        return (e.df, more_records)

    persons_df = prep['persons_df']

    addresses_joined_df = addresses_df.merge(
        persons_df,
        how="left",
        left_on="c_case",
        right_on="c_caserecnumber"
    )

    addresses_joined_df["person_id"] = addresses_joined_df["id_y"]
    addresses_joined_df = addresses_joined_df.drop(columns=["id_y"])
    addresses_joined_df = addresses_joined_df.rename(columns={"id_x": "id"})

    addresses_joined_df = reapply_datatypes_to_fk_cols(
        columns=["person_id"],
        df=addresses_joined_df
    )

    return (addresses_joined_df, True)