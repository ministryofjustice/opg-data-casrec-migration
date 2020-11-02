from entities.deputies.addresses import insert_addresses_deputies
from entities.deputies.persons import insert_persons_deputies


def runner(config, etl2_db):
    """
    | Name      | Running Order | Requires |
    | --------- | ------------- | -------- |
    | persons   | 1             |          |
    | addresses | 2             | persons  |
    |           |               |          |

    """
    insert_persons_deputies(config, etl2_db)
    insert_addresses_deputies(config, etl2_db)


if __name__ == "__main__":
    runner()
