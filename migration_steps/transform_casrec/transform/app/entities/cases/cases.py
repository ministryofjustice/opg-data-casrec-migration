from custom_errors import EmptyDataFrame
from utilities.basic_data_table import get_basic_data_table


def get_cases_chunk(db_config, mapping_file_name, table_definition, sirius_details, chunk_size, offset, prep):
    try:
        df = get_basic_data_table(
            db_config=db_config,
            mapping_file_name=mapping_file_name,
            table_definition=table_definition,
            sirius_details=sirius_details,
            chunk_details={"chunk_size": chunk_size, "offset": offset},
        )

        return (df, True)
    except EmptyDataFrame as e:
        return (e.df, False)

    # persons_query = (
    #     f'select "id", "caserecnumber" from {db_config["target_schema"]}.persons '
    #     f"where \"type\" = 'actor_client';"
    # )
    # persons_df = pd.read_sql_query(persons_query, db_config["db_connection_string"])
    #
    # persons_df = persons_df[["id", "caserecnumber"]]

    # cases_joined_df = cases_df.merge(
    #     persons_df,
    #     how="left",
    #     left_on="caserecnumber",
    #     right_on="caserecnumber",
    # )
    #
    # cases_joined_df["client_id"] = cases_joined_df["id_y"]
    # cases_joined_df = cases_joined_df.drop(columns=["id_y"])
    # cases_joined_df = cases_joined_df.rename(columns={"id_x": "id"})
