import logging

from entities.death.client_death_notifications import insert_client_death_notifications
from entities.death.deputy_death_notifications import insert_deputy_death_notifications
from helpers import log_title, check_entity_enabled

log = logging.getLogger("root")


def runner(target_db, db_config):
    """
    | Name          | Running Order | Requires                   |
    | ------------- | ------------- | -------------------------- |
    | client_death  | 1             | persons (clients)          |
    | deputy_death  | 2             | persons (deputies)         |
    |               |               |                            |

    """

    entity_name = "death"
    if not check_entity_enabled(entity_name):
        return False

    log.info(log_title(message=entity_name))

    # log.debug("Not currently implemented")
    log.debug("insert_client_death_notifications")
    insert_client_death_notifications(
        target_db=target_db,
        db_config=db_config,
    )

    # log.debug("insert_deputy_death_notifications")
    # insert_deputy_death_notifications(
    #     target_db=target_db,
    #     db_config=db_config,
    # )


if __name__ == "__main__":

    runner()
