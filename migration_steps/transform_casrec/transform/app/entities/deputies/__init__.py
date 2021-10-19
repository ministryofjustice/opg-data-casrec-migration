import logging

from entities.deputies.addresses import get_addresses_deputies_chunk, do_addresses_deputies_prep
from entities.deputies.order_deputy import get_order_deputies_records
from entities.deputies.persons import get_persons_deputies_chunk
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
    transformer(db_config, target_db, "deputy_persons", get_persons_deputies_chunk)

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
    transformer(
        db_config,
        target_db,
        "deputy_addresses",
        get_addresses_deputies_chunk,
        do_addresses_deputies_prep
    )

    log.debug("insert_order_deputies")
    transformer(db_config, target_db, "order_deputy", get_order_deputies_records)


if __name__ == "__main__":
    runner()
