import logging

from entities.bonds.bonds_active import insert_bonds_active
from entities.bonds.bonds_dispensed import insert_bonds_dispensed
from helpers import log_title, check_entity_enabled


log = logging.getLogger("root")


def runner(target_db, db_config):
    """
    | Name      | Running Order | Requires |
    | --------- | ------------- | -------- |
    | bonds   | 1               | cases    |
    |           |               |          |
    |           |               |          |

    """

    entity_name = "bonds"
    extra_entities = ["cases"]
    if not check_entity_enabled(entity_name=entity_name, extra_entities=extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_bonds_active")
    insert_bonds_active(
        target_db=target_db, db_config=db_config, mapping_file="bonds_active"
    )

    log.debug("insert_bonds_dispensed")
    insert_bonds_dispensed(
        target_db=target_db, db_config=db_config, mapping_file="bonds_dispensed"
    )


if __name__ == "__main__":

    runner()
