import logging


from helpers import log_title, check_entity_enabled

from entities.remarks.client_notes import insert_client_notes
from entities.remarks.deputy_notes import insert_deputy_notes

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

    log.debug("insert_client_notes")
    insert_client_notes(target_db=target_db, db_config=db_config, mapping_file="client_notes")

    log.debug("insert_deputy_notes")
    insert_deputy_notes(target_db=target_db, db_config=db_config, mapping_file="deputy_notes")


if __name__ == "__main__":
    runner()
