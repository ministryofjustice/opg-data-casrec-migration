from custom_errors import EmptyDataFrame
from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols
from utilities.basic_data_table import get_basic_data_table


def get_bonds_dispensed_chunk(db_config, mapping_file_name, table_definition, sirius_details, chunk_size, offset, prep):
    try:
        bonds_df = get_basic_data_table(
            db_config=db_config,
            mapping_file_name=mapping_file_name,
            table_definition=table_definition,
            sirius_details=sirius_details,
            chunk_details={"chunk_size": chunk_size, "offset": offset},
        )
    except EmptyDataFrame as e:
        more_records = (e.empty_data_frame_type != 'chunk')
        return (e.df, more_records)

    existing_cases_df = prep['existing_cases_df']

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

    return (bonds_cases_joined_df, True)
