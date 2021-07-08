import logging

from entities.warnings.client_nodebtchase_warnings import (
    insert_client_nodebtchase_warnings,
)
from entities.warnings.client_person_warning import insert_client_person_warning
from entities.warnings.client_saarcheck_warnings import insert_client_saarcheck_warnings
from entities.warnings.client_special_warnings import insert_client_special_warnings
from entities.warnings.client_violent_warnings import insert_client_violent_warnings
from entities.warnings.deputy_person_warning import insert_deputy_person_warning
from entities.warnings.deputy_special_warnings import insert_deputy_special_warnings
from entities.warnings.deputy_violent_warnings import insert_deputy_violent_warnings
from helpers import log_title, check_entity_enabled

log = logging.getLogger("root")


def runner(target_db, db_config):
    """
    | Name      | Running Order | Requires |
    | --------- | ------------- | -------- |
    |           |               |          |
    |           |               |          |
    |           |               |          |

    """

    entity_name = "warnings"
    extra_entities = ["clients", "deputies"]
    if not check_entity_enabled(entity_name, extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_client_violent_warnings")
    insert_client_violent_warnings(
        mapping_file="client_violent_warnings",
        target_db=target_db,
        db_config=db_config,
    )
    log.debug("insert_client_special_warnings")
    insert_client_special_warnings(
        mapping_file="client_special_warnings",
        target_db=target_db,
        db_config=db_config,
    )
    log.debug("insert_client_saarcheck_warnings")
    insert_client_saarcheck_warnings(
        mapping_file="client_saarcheck_warnings",
        target_db=target_db,
        db_config=db_config,
    )
    log.debug("insert_client_nodebtchase_warnings")
    insert_client_nodebtchase_warnings(
        mapping_file="client_nodebtchase_warnings",
        target_db=target_db,
        db_config=db_config,
    )

    log.debug("insert_client_person_warning")
    insert_client_person_warning(
        mapping_file="person_warning",
        target_db=target_db,
        db_config=db_config,
    )

    log.debug("insert_deputy_violent_warnings")
    insert_deputy_violent_warnings(
        mapping_file="deputy_violent_warnings",
        target_db=target_db,
        db_config=db_config,
    )
    log.debug("insert_deputy_special_warnings")
    insert_deputy_special_warnings(
        mapping_file="deputy_special_warnings",
        target_db=target_db,
        db_config=db_config,
    )

    log.debug("insert_deputy_person_warning")
    insert_deputy_person_warning(
        mapping_file="person_warning",
        target_db=target_db,
        db_config=db_config,
    )


if __name__ == "__main__":

    runner()
