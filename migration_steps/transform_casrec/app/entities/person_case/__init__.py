import logging

from entities.person_case.person_caseitem import insert_person_caseitem
from utilities.helpers import log_title

log = logging.getLogger("root")


def runner(config, etl2_db):
    """
    | Name                  | Running Order | Requires          |
    | --------------------- | ------------- | ----------------- |
    | person_caseitem       | 1             | persons, cases    |
    |                       |               |                   |

    """

    log.info(log_title(message="person_case"))

    log.debug("insert_person_caseitem")
    insert_person_caseitem(config, etl2_db)


if __name__ == "__main__":
    runner()
