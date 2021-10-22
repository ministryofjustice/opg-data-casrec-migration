import logging

from helpers import log_title, check_entity_enabled
from entities.tasks.tasks import get_tasks_chunk
from entities.tasks.person_task import get_person_task_records
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

    entity_name = "tasks"
    extra_entities = ["deputies", "clients"]
    if not check_entity_enabled(entity_name, extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_tasks")
    transformer(db_config, target_db, "tasks", get_tasks_chunk)

    log.debug("insert_person_task")
    transformer(db_config, target_db, "person_task", get_person_task_records)


if __name__ == "__main__":

    runner()
