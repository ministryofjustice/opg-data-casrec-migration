import logging

from entities.notes.notes import insert_notes
from entities.notes.persons_note import insert_person_notes
from utilities.helpers import log_title

log = logging.getLogger("root")


def runner(config, etl2_db):
    """
    | Name          | Running Order | Requires |
    | ------------- | ------------- | -------- |
    | notes         | 1             |          |
    | person_notes  | 2             | notes    |
    |               |               |          |

    """

    log.info(log_title(message="notes"))

    log.debug("insert_notes")
    insert_notes(config, etl2_db)

    log.debug("insert_person_notes")
    insert_person_notes(config, etl2_db)


if __name__ == "__main__":
    runner()
