import psycopg2
import pandas as pd

definition = {
    "destination_table_name": "person_caseitem",
}


def insert_person_caseitem_clients(config, etl2_db):

    persons_query = (
        f'select "id", "caserecnumber" from etl2.persons '
        f"where \"type\" = 'actor_client';"
    )
    persons_df = pd.read_sql_query(
        persons_query, config["etl2_db"]["connection_string"]
    )

    cases_query = f'select "id", "caserecnumber" from etl2.cases;'
    cases_df = pd.read_sql_query(cases_query, config["etl2_db"]["connection_string"])

    person_caseitem_df = cases_df.merge(
        persons_df,
        how="left",
        left_on="caserecnumber",
        right_on="caserecnumber",
        suffixes=["_case", "_person"],
    )

    person_caseitem_df = person_caseitem_df.drop(columns=["caserecnumber"])
    person_caseitem_df = person_caseitem_df.rename(
        columns={"id_case": "case_id", "id_person": "person_id"}
    )

    etl2_db.insert_data(
        table_name=definition["destination_table_name"], df=person_caseitem_df
    )
