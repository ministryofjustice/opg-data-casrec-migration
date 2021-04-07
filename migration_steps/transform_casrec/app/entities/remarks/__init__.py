import logging


from helpers import log_title, check_entity_enabled

from entities.remarks.caseitem_note import insert_caseitem_note
from entities.remarks.notes import insert_notes

log = logging.getLogger("root")


def runner(target_db, db_config):
    """
    | Name          | Running Order  | Requires     |
    | ------------- | -------------- | ------------ |
    | notes         | 1              |              |
    | caseitem_note | 2              | notes, cases |
    |               |                |              |

    """

    entity_name = "remarks"
    extra_entities = ["cases"]
    if not check_entity_enabled(entity_name, extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_notes")
    insert_notes(target_db=target_db, db_config=db_config)

    log.debug("insert_caseitem_note")
    insert_caseitem_note(target_db=target_db, db_config=db_config)


if __name__ == "__main__":

    runner()
