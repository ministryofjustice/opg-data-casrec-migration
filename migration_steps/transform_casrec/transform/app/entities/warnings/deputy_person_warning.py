import pandas as pd

from transform_data.apply_datatypes import reapply_datatypes_to_fk_cols


def get_deputy_person_warning_records(
    db_config,
    mapping_file_name,
    table_definition,
    sirius_details,
    chunk_size,
    offset,
    prep
):
    deputy_warning_query = f"""
        select * from {db_config["target_schema"]}.warnings
        where casrec_table_name = 'deputy';
    """

    deputy_warning_df = pd.read_sql_query(
        deputy_warning_query, db_config["db_connection_string"]
    )

    if len(deputy_warning_df) == 0:
        return (deputy_warning_df, False)

    deputys_query = (
        f'select "id", "c_deputy_no" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_deputy';"
    )

    deputys_df = pd.read_sql_query(deputys_query, db_config["db_connection_string"])

    deputy_warning_df = deputy_warning_df[["id", "c_deputy_no"]]

    deputy_warning_df = deputy_warning_df.merge(
        deputys_df,
        how="left",
        left_on="c_deputy_no",
        right_on="c_deputy_no",
        suffixes=["_warning", "_deputy"],
    )

    deputy_warning_df = deputy_warning_df.rename(
        columns={"id_warning": "warning_id", "id_deputy": "person_id"}
    )
    deputy_warning_df["casrec_details"] = "{}"

    deputy_warning_df = reapply_datatypes_to_fk_cols(
        columns=["person_id", "warning_id"], df=deputy_warning_df
    )

    return (deputy_warning_df, False)
