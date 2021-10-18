from custom_errors import EmptyDataFrame
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table


def get_phonenumbers_clients_chunk(db_config, mapping_file_name, table_definition, sirius_details, chunk_size, offset, prep):
    try:
        phonenos_df = get_basic_data_table(
            db_config=db_config,
            mapping_file_name=mapping_file_name,
            table_definition=table_definition,
            sirius_details=sirius_details,
            chunk_details={"chunk_size": chunk_size, "offset": offset},
        )
    except EmptyDataFrame as e:
        return (e.df, False)

    persons_df = prep['persons_df']

    phonenos_joined_df = phonenos_df.merge(
        persons_df,
        how="left",
        left_on="c_case",
        right_on="c_caserecnumber"
    )

    phonenos_joined_df["person_id"] = phonenos_joined_df["id_y"]
    phonenos_joined_df = phonenos_joined_df.drop(columns=["id_y"])
    phonenos_joined_df = phonenos_joined_df.rename(columns={"id_x": "id"})

    phonenos_joined_df = reapply_datatypes_to_fk_cols(
        columns=["person_id"],
        df=phonenos_joined_df
    )

    return (phonenos_joined_df, True)