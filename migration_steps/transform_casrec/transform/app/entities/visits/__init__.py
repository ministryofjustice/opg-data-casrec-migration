import logging

from entities.visits.visits import insert_visits
from helpers import log_title, check_entity_enabled

log = logging.getLogger("root")


def runner(target_db, db_config):
    """
    | Name      | Running Order | Requires |
    | --------- | ------------- | -------- |
    |           |               |          |
    |           |               |          |
    |           |               |          |

    """

    entity_name = "visits"
    if not check_entity_enabled(entity_name):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_persons_clients")
    insert_visits(
        target_db=target_db,
        db_config=db_config,
    )


if __name__ == "__main__":

    runner()
