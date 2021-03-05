import logging

from entities.supervision_level.supervision_level_log import (
    insert_supervision_level_log,
)
from helpers import log_title

log = logging.getLogger("root")


def runner(db_config, target_db):
    """
    | Name                      | Running Order | Requires |
    | --------------------------| ------------- | -------- |
    | supervision_level_log     | 1             | cases    |
    |                           |               |          |

    """

    log.info(log_title(message="supervision level"))

    log.debug("insert_supervision_level_log")
    insert_supervision_level_log(
        db_config, target_db, mapping_file_name="supervision_level_log_mapping"
    )


if __name__ == "__main__":
    runner()
