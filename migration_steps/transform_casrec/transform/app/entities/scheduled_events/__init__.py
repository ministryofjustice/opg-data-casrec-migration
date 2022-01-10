import logging

from entities.scheduled_events.scheduled_events_reporting import (
    insert_scheduled_events_reporting,
)
from helpers import log_title, check_entity_enabled

log = logging.getLogger("root")


def runner(target_db, db_config):
    """
    | Name                              | Running Order | Requires  |
    | --------------------------------- | ------------- | --------- |
    | insert_scheduled_events_reporting | 1             | reporting |

    """

    entity_name = "scheduled_events"
    extra_entities = ["reporting"]
    if not check_entity_enabled(entity_name=entity_name, extra_entities=extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_scheduled_events_reporting")
    insert_scheduled_events_reporting(
        mapping_file="scheduled_events_reporting",
        target_db=target_db,
        db_config=db_config,
    )


if __name__ == "__main__":

    runner()
