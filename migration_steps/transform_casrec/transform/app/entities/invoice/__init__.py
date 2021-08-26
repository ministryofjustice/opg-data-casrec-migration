import logging


from helpers import log_title, check_entity_enabled
from entities.invoice.finance_invoice import insert_finance_invoice

log = logging.getLogger("root")


def runner(target_db, db_config):
    """
    | Name                   | Running Order | Requires |
    | ---------------------- | ------------- | -------- |
    | finance_invoice_ad     | 1             |          |
    | finance_invoice_non_ad | 2             |          |

    """

    entity_name = "invoice"
    extra_entities = []
    if not check_entity_enabled(entity_name=entity_name, extra_entities=extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_finance_invoice - AD")
    insert_finance_invoice(
        target_db=target_db, db_config=db_config, mapping_file="finance_invoice_ad"
    )

    log.debug("insert_finance_invoice - non-AD")
    insert_finance_invoice(
        target_db=target_db, db_config=db_config, mapping_file="finance_invoice_non_ad"
    )


if __name__ == "__main__":

    runner()
