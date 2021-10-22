import logging

from entities.supervision_level.supervision_level_log import (
    get_supervision_level_log_chunk, do_supervision_level_log_prep
)
from helpers import log_title, check_entity_enabled
from transform_data.transformer import transformer


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
    transformer(
        db_config,
        target_db,
        "supervision_level_log",
        get_supervision_level_log_chunk,
        do_supervision_level_log_prep
    )


if __name__ == "__main__":
    runner()
