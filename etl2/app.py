from sqlalchemy import create_engine

from helpers import print_result, insert_result
from tables.persons_client import final as persons_client
from tables.addresses_client import final as addresses_client
from tables.cases import final as cases
from tables.notes import final as notes
from tables.persons_note import final as caseitem_note
from tables.person_caseitem_client import final as person_caseitem

debug_mode = False

if __name__ == "__main__":

    persons_client_df = persons_client()
    if debug_mode:
        print_result(persons_client_df, "persons")
    else:
        insert_result(persons_client_df, "persons")

    addresses_client_df = addresses_client()
    if debug_mode:
        print_result(addresses_client_df, "addresses")
    else:
        insert_result(addresses_client_df, "addresses")

    cases_df = cases()
    if debug_mode:
        print_result(cases_df, "cases")
    else:
        insert_result(cases_df, "cases")

    person_caseitem_df = person_caseitem(persons_client_df, cases_df)
    if debug_mode:
        print_result(person_caseitem_df, "person_caseitem")
    else:
        insert_result(person_caseitem_df, "person_caseitem")

    notes_df = notes()
    if debug_mode:
        print_result(notes_df, "notes")
    else:
        insert_result(notes_df, "notes")

    person_note_df = caseitem_note(persons_client_df, notes_df)
    if debug_mode:
        print_result(person_note_df, "person_note")
    else:
        insert_result(person_note_df, "person_note")
