import logging

from entities.visits.visits import get_visits_chunk, do_visits_prep
from helpers import log_title, check_entity_enabled
from transform_data.transformer import transformer


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

    log.debug("insert_visits")
    transformer(db_config, target_db, "visits", get_visits_chunk, do_visits_prep)


if __name__ == "__main__":

    runner()
