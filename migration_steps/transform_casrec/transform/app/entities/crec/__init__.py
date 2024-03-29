import logging

from entities.crec.persons import insert_persons_crec
from helpers import log_title, check_entity_enabled

log = logging.getLogger("root")


def runner(target_db, db_config):
    """
    | Name      | Running Order | Requires |
    | --------- | ------------- | -------- |
    |  crec     | 1             | persons  |
    |           |               |          |
    |           |               |          |

    """

    entity_name = "crec"
    if not check_entity_enabled(entity_name):
        return False

    log.info(log_title(message=entity_name))

    log.info("Inserting crec_persons")
    insert_persons_crec(
        mapping_file="crec_persons",
        target_db=target_db,
        db_config=db_config,
    )


if __name__ == "__main__":

    runner()
