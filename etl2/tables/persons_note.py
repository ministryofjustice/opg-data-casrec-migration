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

    notes_query = f"select * from etl2.notes;"
    notes_df = pd.read_sql_query(notes_query, casrec_db_connection)

    notes_query = f'select "rct", "Case" from etl1.remarks;'
    notes_with_case_df = pd.read_sql_query(notes_query, casrec_db_connection)

    notes_df = notes_df.merge(
        notes_with_case_df, how="left", left_on="casrec_id", right_on="rct"
    )

    person_note_df = notes_df.merge(
        persons_df,
        how="left",
        left_on="Case",
        right_on="caserecnumber",
        suffixes=["_note", "_person"],
    )

    person_note_df = person_note_df.rename(
        columns={"id_person": "person_id", "id_note": "note_id"}
    )

    person_note_df = person_note_df[["person_id", "note_id"]]
    return person_note_df
