import logging

# from entities.deputies.addresses import insert_addresses_deputies
from entities.deputies.order_deputy import insert_order_deputies
from entities.deputies.addresses import insert_addresses_deputies
from entities.deputies.persons import insert_persons_deputies
from helpers import log_title

from entities.deputies.phonenumbers_daytime import insert_phonenumbers_deputies_daytime
from entities.deputies.phonenumbers_evening import insert_phonenumbers_deputies_evening

log = logging.getLogger("root")


def runner(target_db, db_config):
    """
    | Name          | Running Order | Requires |
    | ---------     | ------------- | -------- |
    | persons       | 1             |          |
    | phonenumbers  | 2             | persons  |
    |               |               |          |

    """

    log.info(log_title(message="deputies"))

    log.debug("insert_persons_deputies")
    insert_persons_deputies(target_db=target_db, db_config=db_config)

    log.debug("insert_phonenumbers_deputies")
    insert_phonenumbers_deputies_daytime(
        target_db=target_db,
        db_config=db_config,
    )
    insert_phonenumbers_deputies_evening(
        target_db=target_db,
        db_config=db_config,
    )

    log.debug("insert_addresses_deputies")
    insert_addresses_deputies(
        target_db=target_db,
        db_config=db_config,
    )

    log.debug("insert_order_deputies")
    insert_order_deputies(
        target_db=target_db,
        db_config=db_config,
    )


if __name__ == "__main__":
    runner()
