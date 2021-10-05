import logging

from entities.clients.addresses import insert_addresses_clients
from entities.clients.person_caseitem import insert_person_caseitem
from entities.clients.persons import insert_persons_clients
from entities.clients.phonenumbers import insert_phonenumbers_clients
from helpers import log_title, check_entity_enabled

log = logging.getLogger("root")


def runner(target_db, db_config):
    """
    | Name      | Running Order | Requires |
    | --------- | ------------- | -------- |
    | persons   | 1             |          |
    | addresses | 2             | persons  |
    |           |               |          |

    """

    entity_name = "clients"
    extra_entities = ["cases", "deputies"]
    if not check_entity_enabled(entity_name, extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_persons_clients")
    insert_persons_clients(
        mapping_file="client_persons",
        target_db=target_db,
        db_config=db_config,
    )

    log.debug("insert_addresses_clients")
    insert_addresses_clients(
        mapping_file="client_addresses",
        target_db=target_db,
        db_config=db_config,
    )

    log.debug("insert_phonenumbers_clients")
    insert_phonenumbers_clients(
        mapping_file="client_phonenumbers",
        target_db=target_db,
        db_config=db_config,
    )
    log.debug("insert_person_caseitem")
    insert_person_caseitem(
        target_db=target_db, db_config=db_config, mapping_file="person_caseitem"
    )


if __name__ == "__main__":

    runner()
