import logging


from helpers import log_title, check_entity_enabled
from entities.fee_reductions.fee_reductions import insert_fee_reductions

log = logging.getLogger("root")


def runner(target_db, db_config):
    """
    | Name                   | Running Order | Requires |
    | ---------------------- | ------------- | -------- |
    | finance_remissions     | 1             |          |
    | finance_exemptions     | 2             |          |

    """

    entity_name = "fee_reductions"
    extra_entities = []
    if not check_entity_enabled(entity_name=entity_name, extra_entities=extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_fee_reductions - remissions")
    insert_fee_reductions(
        target_db=target_db, db_config=db_config, mapping_file="finance_remissions"
    )

    log.debug("insert_fee_reductions - exemptions")
    insert_fee_reductions(
        target_db=target_db, db_config=db_config, mapping_file="finance_exemptions"
    )


if __name__ == "__main__":

    runner()
