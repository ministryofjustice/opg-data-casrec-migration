from custom_errors import EmptyDataFrame
from utilities.basic_data_table import get_basic_data_table


def get_persons_deputies_chunk(
    db_config,
    mapping_file_name,
    table_definition,
    sirius_details,
    chunk_size,
    offset,
    prep
):
    try:
        persons_df = get_basic_data_table(
            db_config=db_config,
            mapping_file_name=mapping_file_name,
            table_definition=table_definition,
            sirius_details=sirius_details,
            chunk_details={"chunk_size": chunk_size, "offset": offset},
        )
    except EmptyDataFrame as e:
        more_records = (e.empty_data_frame_type != 'chunk')
        return (e.df, more_records)

    return (persons_df, True)
