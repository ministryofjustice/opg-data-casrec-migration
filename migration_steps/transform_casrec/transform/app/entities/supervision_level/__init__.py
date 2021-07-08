import logging

from entities.supervision_level.supervision_level_log import (
    insert_supervision_level_log,
)
from helpers import log_title, check_entity_enabled

log = logging.getLogger("root")


def runner(db_config, target_db):
    """
    | Name                      | Running Order | Requires |
    | --------------------------| ------------- | -------- |
    | supervision_level_log     | 1             | cases    |
    |                           |               |          |

    """

    entity_name = "supervision_level"
    extra_entities = ["cases"]
    if not check_entity_enabled(entity_name, extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_supervision_level_log")
    insert_supervision_level_log(
        db_config=db_config, target_db=target_db, mapping_file="supervision_level_log"
    )


if __name__ == "__main__":
    runner()
