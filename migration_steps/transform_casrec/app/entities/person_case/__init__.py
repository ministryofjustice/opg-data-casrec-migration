from entities.person_case.person_caseitem import insert_person_caseitem


def runner(config, etl2_db):
    """
    | Name                  | Running Order | Requires          |
    | --------------------- | ------------- | ----------------- |
    | person_caseitem       | 1             | persons, cases    |
    |                       |               |                   |

    """
    insert_person_caseitem(config, etl2_db)


if __name__ == "__main__":
    runner()
