import logging

from entities.cases.cases import insert_cases


from helpers import log_title, check_entity_enabled

log = logging.getLogger("root")


def runner(db_config, target_db):
    """
    | Name                      | Running Order | Requires                  |
    | ------------------------- | ------------- | ------------------------- |
    | cases                     | 1             |                           |
    |                           |               |                           |

    """

    entity_name = "cases"
    extra_entities = []
    if not check_entity_enabled(entity_name, extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_cases")
    insert_cases(target_db=target_db, db_config=db_config, mapping_file="cases")


if __name__ == "__main__":
    runner()
