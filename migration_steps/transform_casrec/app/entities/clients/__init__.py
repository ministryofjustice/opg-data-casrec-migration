import logging

from entities.clients.addresses import insert_addresses_clients
from entities.clients.persons import insert_persons_clients
from entities.clients.phonenumbers import insert_phonenumbers_clients
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

    log.info(log_title(message="clients"))

    log.debug("insert_persons_clients")
    insert_persons_clients(config, etl2_db)

    log.debug("insert_addresses_clients")
    insert_addresses_clients(config, etl2_db)

    log.debug("insert_phonenumbers_clients")
    insert_phonenumbers_clients(config, etl2_db)


if __name__ == "__main__":

    runner()
