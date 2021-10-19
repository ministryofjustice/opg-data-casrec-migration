import logging

from helpers import log_title, check_entity_enabled
from entities.invoice.finance_invoice import do_finance_invoice_prep, get_finance_invoice_chunk
from transform_data.transformer import transformer


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
    transformer(db_config, target_db, "finance_invoice_ad", get_finance_invoice_chunk, do_finance_invoice_prep)

    log.debug("insert_finance_invoice - non-AD")
    transformer(db_config, target_db, "finance_invoice_non_ad", get_finance_invoice_chunk, do_finance_invoice_prep)


if __name__ == "__main__":

    runner()
