import logging

from entities.remarks.client_notes import get_client_notes_chunk, do_client_notes_prep
from entities.remarks.deputy_notes import get_deputy_notes_chunk, do_deputy_notes_prep
from helpers import log_title, check_entity_enabled
from transform_data.transformer import transformer


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
    transformer(db_config, target_db, "client_notes", get_client_notes_chunk, do_client_notes_prep)

    log.debug("insert_deputy_notes")
    transformer(db_config, target_db, "deputy_notes", get_deputy_notes_chunk, do_deputy_notes_prep)

if __name__ == "__main__":
    runner()
