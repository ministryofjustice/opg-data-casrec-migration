from entities.order_deputy.order_deputy import insert_order_deputy


def runner(config, etl2_db):
    """
    | Name                  | Running Order | Requires          |
    | --------------------- | ------------- | ----------------- |
    | order_deputy          | 1             | deputies, cases   |
    |                       |               |                   |

    """
    insert_order_deputy(config, etl2_db)


if __name__ == "__main__":
    runner()
