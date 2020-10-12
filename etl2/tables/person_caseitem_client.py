import psycopg2
import pandas as pd

casrec_db_connection = psycopg2.connect(
    "host=localhost port=6666 "
    "dbname=casrecmigration "
    "user=casrec "
    "password=casrec"
)


def final():

    # persons_df = persons_df[["id", "caserecnumber"]]

    persons_query = f'select "id", "caserecnumber" from etl2.persons;'
    persons_df = pd.read_sql_query(persons_query, casrec_db_connection)

    cases_query = f'select "id", "caserecnumber" from etl2.cases;'
    cases_df = pd.read_sql_query(cases_query, casrec_db_connection)

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

    return person_caseitem_df
