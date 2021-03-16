import logging

from entities.clients.addresses import insert_addresses_clients
from entities.clients.persons import insert_persons_clients
from entities.clients.phonenumbers import insert_phonenumbers_clients
from helpers import log_title

log = logging.getLogger("root")


def runner(target_db, db_config):
    """
    | Name      | Running Order | Requires |
    | --------- | ------------- | -------- |
    | persons   | 1             |          |
    | addresses | 2             | persons  |
    |           |               |          |

    """

    log.info(log_title(message="clients"))

    log.debug("insert_persons_clients")
    insert_persons_clients(
        target_db=target_db,
        db_config=db_config,
    )

    log.debug("insert_addresses_clients")
    insert_addresses_clients(
        target_db=target_db,
        db_config=db_config,
    )

    log.debug("insert_phonenumbers_clients")
    insert_phonenumbers_clients(
        target_db=target_db,
        db_config=db_config,
    )


if __name__ == "__main__":

    runner()
