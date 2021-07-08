import logging

from entities.reporting.annual_report_lodging_details import (
    insert_annual_report_lodging_details,
)
from entities.reporting.annual_report_logs import insert_annual_report_logs
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

    entity_name = "reporting"
    if not check_entity_enabled(entity_name):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_annual_report_logs")
    insert_annual_report_logs(
        mapping_file="annual_report_logs",
        target_db=target_db,
        db_config=db_config,
    )

    log.debug("insert_annual_report_lodging_details")
    insert_annual_report_lodging_details(
        mapping_file="annual_report_lodging_details",
        target_db=target_db,
        db_config=db_config,
    )


if __name__ == "__main__":

    runner()
