import logging


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

    entity_name = "reporting"
    if not check_entity_enabled(entity_name):
        return False

    log.info(log_title(message=entity_name))

    log.debug("Not currently implemented")


if __name__ == "__main__":

    runner()
