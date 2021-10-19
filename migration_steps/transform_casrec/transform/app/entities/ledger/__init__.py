import logging

from helpers import log_title, check_entity_enabled
from entities.ledger.finance_ledger import get_finance_ledger_credits_chunk, do_finance_ledger_credits_prep
from transform_data.transformer import transformer


log = logging.getLogger("root")

def runner(target_db, db_config):
    """
    | Name                   | Running Order | Requires |
    | ---------------------- | ------------- | -------- |
    | finance_ledger_credits | 1             |          |

    """

    entity_name = "ledger"
    extra_entities = []
    if not check_entity_enabled(entity_name=entity_name, extra_entities=extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_finance_ledger_credits")
    transformer(
        db_config,
        target_db,
        "finance_ledger_credits",
        get_finance_ledger_credits_chunk,
        do_finance_ledger_credits_prep
    )


if __name__ == "__main__":

    runner()
