import psycopg2
import pandas as pd

definition = {
    "destination_table_name": "person_note",
}


def insert_person_notes(config, etl2_db):

    persons_query = f'select "id", "caserecnumber" from etl2.persons;'
    persons_df = pd.read_sql_query(
        persons_query, config["etl2_db"]["connection_string"]
    )

    notes_query = f'select "id", "c_case" from etl2.notes;'
    notes_df = pd.read_sql_query(notes_query, config["etl2_db"]["connection_string"])

    person_note_df = notes_df.merge(
        persons_df,
        how="left",
        left_on="c_case",
        right_on="caserecnumber",
        suffixes=["_note", "_person"],
    )

    person_note_df = person_note_df.rename(
        columns={"id_person": "person_id", "id_note": "note_id"}
    )

    person_note_df = person_note_df[["person_id", "note_id"]]

    etl2_db.insert_data(
        table_name=definition["destination_table_name"], df=person_note_df
    )
