import logging

from entities.deputies.addresses import insert_addresses_deputies
from entities.deputies.persons import insert_persons_deputies
from utilities.helpers import log_title

log = logging.getLogger("root")


def runner(config, etl2_db):
    """
    | Name      | Running Order | Requires |
    | --------- | ------------- | -------- |
    | persons   | 1             |          |
    | addresses | 2             | persons  |
    |           |               |          |

    """

    log.info(log_title(message="deputies"))

    log.debug("insert_persons_deputies")
    insert_persons_deputies(config, etl2_db)

    log.debug("insert_addresses_deputies")
    insert_addresses_deputies(config, etl2_db)


if __name__ == "__main__":
    runner()
