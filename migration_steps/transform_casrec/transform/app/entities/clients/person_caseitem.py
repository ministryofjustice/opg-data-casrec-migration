import pandas as pd


# raises EmptyDataFrame if a query fails
# note that most of the arguments passed are ignored as we're not chunking anything
def get_person_caseitem_records(db_config, mapping_file_name, table_definition, sirius_details, chunk_size, offset, prep):
    persons_df = prep['persons_df']

    cases_query = (
        f'select "id", "caserecnumber" from {db_config["target_schema"]}.cases;'
    )
    cases_df = pd.read_sql_query(cases_query, db_config["db_connection_string"])

    person_caseitem_df = cases_df.merge(
        persons_df,
        how="left",
        left_on="caserecnumber",
        right_on="c_caserecnumber",
        suffixes=["_case", "_person"],
    )

    person_caseitem_df = person_caseitem_df.drop(columns=["caserecnumber"])
    person_caseitem_df = person_caseitem_df.rename(
        columns={"id_case": "caseitem_id", "id_person": "person_id"}
    )

    person_caseitem_df["casrec_details"] = "{}"

    # this is a one-off non-chunked frame, so more_records is always False
    return (person_caseitem_df, False)
