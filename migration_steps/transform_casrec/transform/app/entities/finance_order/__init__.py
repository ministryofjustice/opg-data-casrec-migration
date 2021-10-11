import logging

from helpers import log_title, check_entity_enabled
from entities.finance_order.finance_order import insert_finance_order

log = logging.getLogger("root")


def runner(target_db, db_config):
    """
    | Name                 | Running Order | Requires |
    | ---------------------| ------------- | -------- |
    | finance_order_active | 1             |          |
    | finance_order_closed | 2             |          |

    """

    entity_name = "finance_order"
    extra_entities = []
    if not check_entity_enabled(entity_name=entity_name, extra_entities=extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_finance_order - Active")
    insert_finance_order(
        target_db=target_db, db_config=db_config, mapping_file="finance_order_active"
    )

    log.debug("insert_finance_order - Closed")
    insert_finance_order(
        target_db=target_db, db_config=db_config, mapping_file="finance_order_closed"
    )


if __name__ == "__main__":

    runner()
