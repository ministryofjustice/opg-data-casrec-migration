import logging

from helpers import log_title, check_entity_enabled
from entities.ledger_allocation.finance_allocation import (
    do_finance_allocation_credits_prep, get_finance_allocation_credits_chunk
)
from transform_data.transformer import transformer


log = logging.getLogger("root")

def runner(target_db, db_config):
    """
    | Name                       | Running Order | Requires |
    | -------------------------- | ------------- | -------- |
    | finance_allocation_credits | 1             |          |

    """

    entity_name = "ledger"
    extra_entities = []
    if not check_entity_enabled(entity_name=entity_name, extra_entities=extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_finance_allocation_credits")
    transformer(
        db_config,
        target_db,
        "finance_allocation_credits",
        get_finance_allocation_credits_chunk,
        do_finance_allocation_credits_prep
    )


if __name__ == "__main__":

    runner()
