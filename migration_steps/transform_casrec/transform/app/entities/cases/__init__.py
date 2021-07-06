import logging

from entities.cases.cases import insert_cases
from entities.cases.person_caseitem import insert_person_caseitem

from helpers import log_title, check_entity_enabled

log = logging.getLogger("root")


def runner(db_config, target_db):
    """
    | Name                      | Running Order | Requires                  |
    | ------------------------- | ------------- | ------------------------- |
    | cases                     | 1             |                           |
    | person_caseitem           | 2             | cases, clients_persons    |

    """

    entity_name = "cases"
    extra_entities = ["clients"]
    if not check_entity_enabled(entity_name, extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_cases")
    insert_cases(target_db=target_db, db_config=db_config, mapping_file="cases")

    log.debug("insert_person_caseitem")
    insert_person_caseitem(
        target_db=target_db, db_config=db_config, mapping_file="person_caseitem"
    )


if __name__ == "__main__":
    runner()
