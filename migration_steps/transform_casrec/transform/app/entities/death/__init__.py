import logging

from entities.death.client_death_notifications import get_client_death_notifications_chunk, do_clients_prep
from entities.death.deputy_death_notifications import get_deputy_death_notifications_chunk, do_deputies_prep
from helpers import log_title, check_entity_enabled
from transform_data.transformer import transformer


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
    extra_entities = ["clients", "deputies"]
    if not check_entity_enabled(entity_name, extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.info("Inserting client_death_notifications")
    transformer(
        db_config,
        target_db,
        "client_death_notifications",
        get_client_death_notifications_chunk,
        do_clients_prep
    )

    log.info("Inserting deputy_death_notifications")
    transformer(
        db_config,
        target_db,
        "deputy_death_notifications",
        get_deputy_death_notifications_chunk,
        do_deputies_prep
    )

if __name__ == "__main__":

    runner()
