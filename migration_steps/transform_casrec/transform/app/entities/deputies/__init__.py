import logging

from entities.deputies.order_deputy import insert_order_deputies
from entities.deputies.addresses import insert_addresses_deputies
from entities.deputies.persons import insert_persons_deputies
from entities.deputies.phonenumbers import get_phonenumbers_deputies_chunk, do_deputies_prep
from helpers import log_title, check_entity_enabled
from transform_data.transformer import transformer


log = logging.getLogger("root")

def runner(target_db, db_config):
    """
    | Name          | Running Order | Requires |
    | ---------     | ------------- | -------- |
    | persons       | 1             |          |
    | phonenumbers  | 2             | persons  |
    |               |               |          |

    """

    entity_name = "deputies"
    extra_entities = ["cases"]
    if not check_entity_enabled(entity_name, extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_persons_deputies")
    insert_persons_deputies(
        target_db=target_db, db_config=db_config, mapping_file="deputy_persons"
    )

    log.debug("insert_phonenumbers_deputies - daytime")
    transformer(
        db_config,
        target_db,
        "deputy_daytime_phonenumbers",
        get_phonenumbers_deputies_chunk,
        do_deputies_prep
    )

    log.debug("insert_phonenumbers_deputies - evening")
    transformer(
        db_config,
        target_db,
        "deputy_evening_phonenumbers",
        get_phonenumbers_deputies_chunk,
        do_deputies_prep
    )

    log.debug("insert_addresses_deputies")
    insert_addresses_deputies(
        mapping_file="deputy_addresses",
        target_db=target_db,
        db_config=db_config,
    )

    log.debug("insert_order_deputies")
    insert_order_deputies(
        mapping_file="order_deputy",
        target_db=target_db,
        db_config=db_config,
    )


if __name__ == "__main__":
    runner()
