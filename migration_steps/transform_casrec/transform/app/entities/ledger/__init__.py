import logging


from helpers import log_title, check_entity_enabled
from entities.ledger.finance_ledger import insert_finance_ledger_credits

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
    insert_finance_ledger_credits(
        target_db=target_db, db_config=db_config, mapping_file="finance_ledger_credits"
    )


if __name__ == "__main__":

    runner()
