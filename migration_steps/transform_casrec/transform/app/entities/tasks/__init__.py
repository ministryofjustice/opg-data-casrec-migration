import logging

from helpers import log_title, check_entity_enabled
from entities.tasks.tasks import insert_tasks

log = logging.getLogger("root")

def runner(target_db, db_config):
    """
    | Name      | Running Order | Requires |
    | --------- | ------------- | -------- |
    |           |               |          |
    |           |               |          |
    |           |               |          |

    """

    entity_name = "tasks"
    extra_entities = ["deputies", "clients"]
    if not check_entity_enabled(entity_name, extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_tasks")
    insert_tasks(target_db=target_db, db_config=db_config, mapping_file="tasks")


if __name__ == "__main__":

    runner()
