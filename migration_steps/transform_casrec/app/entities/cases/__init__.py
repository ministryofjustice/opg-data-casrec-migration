import logging

from entities.cases.cases import insert_cases
from entities.cases.person_caseitem import insert_person_caseitem

from helpers import log_title

log = logging.getLogger("root")


def runner(db_config, target_db):
    """
    | Name                      | Running Order | Requires                  |
    | ------------------------- | ------------- | ------------------------- |
    | cases                     | 1             |                           |
    | person_caseitem           | 2             | cases, clients_persons    |

    """

    log.info(log_title(message="cases"))

    log.debug("insert_cases")
    insert_cases(target_db=target_db, db_config=db_config)

    log.debug("insert_person_caseitem")
    insert_person_caseitem(
        target_db=target_db,
        db_config=db_config,
    )


if __name__ == "__main__":
    runner()
