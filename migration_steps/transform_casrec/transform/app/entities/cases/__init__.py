import logging

from entities.cases.cases import get_cases_chunk
from helpers import log_title, check_entity_enabled
from transform_data.transformer import transformer


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
    transformer(db_config, target_db, "cases", get_cases_chunk)


if __name__ == "__main__":
    runner()
