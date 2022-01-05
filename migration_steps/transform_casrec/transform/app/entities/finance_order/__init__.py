import logging

from helpers import log_title, check_entity_enabled
from entities.finance_order.finance_order import insert_finance_order

log = logging.getLogger("root")


def runner(target_db, db_config):
    """
    | Name          | Running Order | Requires |
    | --------------| ------------- | -------- |
    | finance_order | 1             |          |
    """

    entity_name = "finance_order"
    extra_entities = ["cases"]
    if not check_entity_enabled(entity_name=entity_name, extra_entities=extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_finance_order")
    insert_finance_order(
        target_db=target_db, db_config=db_config, mapping_file="finance_order"
    )


if __name__ == "__main__":

    runner()
