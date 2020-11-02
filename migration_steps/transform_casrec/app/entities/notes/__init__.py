from entities.notes.notes import insert_notes
from entities.notes.persons_note import insert_person_notes


def runner(config, etl2_db):
    """
    | Name          | Running Order | Requires |
    | ------------- | ------------- | -------- |
    | notes         | 1             |          |
    | person_notes  | 2             | notes    |
    |               |               |          |

    """
    insert_notes(config, etl2_db)
    insert_person_notes(config, etl2_db)


if __name__ == "__main__":
    runner()
