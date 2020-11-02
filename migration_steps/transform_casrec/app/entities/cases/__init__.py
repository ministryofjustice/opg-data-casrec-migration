from entities.cases.cases import insert_cases


def runner(config, etl2_db):
    """
    | Name      | Running Order | Requires |
    | --------- | ------------- | -------- |
    | cases     | 1             |          |
    |           |               |          |

    """
    insert_cases(config, etl2_db)


if __name__ == "__main__":
    runner()
