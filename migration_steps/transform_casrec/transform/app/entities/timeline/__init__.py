import logging

from entities.timeline.timeline_event import insert_timeline_events
from entities.timeline.person_timeline import insert_person_timeline
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

    entity_name = "timeline"
    extra_entities = ["cases", "clients", "deputies"]
    if not check_entity_enabled(entity_name=entity_name, extra_entities=extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_timeline_events_migration")
    insert_timeline_events(
        mapping_file="timeline_event",
        target_db=target_db,
        db_config=db_config,
        event_sub_type="migration",
    )

    log.debug("insert_timeline_events_archive")
    insert_timeline_events(
        mapping_file="timeline_event",
        target_db=target_db,
        db_config=db_config,
        event_sub_type="archive",
    )

    log.debug("insert_person_timeline")
    insert_person_timeline(
        mapping_file="person_timeline",
        target_db=target_db,
        db_config=db_config,
    )


if __name__ == "__main__":
    runner()
