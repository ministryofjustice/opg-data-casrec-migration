from entities.clients.addresses import insert_addresses_clients
from entities.clients.persons import insert_persons_clients


def runner(config, etl2_db):
    """
    | Name      | Running Order | Requires |
    | --------- | ------------- | -------- |
    | persons   | 1             |          |
    | addresses | 2             | persons  |
    |           |               |          |

    """
    insert_persons_clients(config, etl2_db)
    insert_addresses_clients(config, etl2_db)


if __name__ == "__main__":
    runner()
