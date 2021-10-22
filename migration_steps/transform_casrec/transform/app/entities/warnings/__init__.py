import logging

from custom_errors import EmptyDataFrame
from entities.warnings.client_person_warning import get_client_person_warning_records
from entities.warnings.deputy_person_warning import get_deputy_person_warning_records
from helpers import log_title, check_entity_enabled
from transform_data.transformer import transformer
from utilities.basic_data_table import get_basic_data_table


log = logging.getLogger("root")

def _get_warnings_chunk(db_config, mapping_file_name, table_definition, sirius_details, chunk_size, offset, prep):
    try:
        warnings_df = get_basic_data_table(
            db_config=db_config,
            mapping_file_name=mapping_file_name,
            table_definition=table_definition,
            sirius_details=sirius_details,
            chunk_details={"chunk_size": chunk_size, "offset": offset},
        )

        return (warnings_df, True)
    except EmptyDataFrame as e:
        more_records = (e.empty_data_frame_type != 'chunk')
        return (e.df, more_records)

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
    transformer(db_config, target_db, "client_violent_warnings", _get_warnings_chunk)

    log.debug("insert_client_saarcheck_warnings")
    transformer(db_config, target_db, "client_saarcheck_warnings", _get_warnings_chunk)

    log.debug("insert_client_special_warnings")
    transformer(db_config, target_db, "client_special_warnings", _get_warnings_chunk)

    log.debug("insert_client_nodebtchase_warnings")
    transformer(db_config, target_db, "client_nodebtchase_warnings", _get_warnings_chunk)

    log.debug("insert_client_person_warning")
    transformer(db_config, target_db, "person_warning", get_client_person_warning_records)

    log.debug("insert_deputy_violent_warnings")
    transformer(db_config, target_db, "deputy_violent_warnings", _get_warnings_chunk)

    log.debug("insert_deputy_special_warnings")
    transformer(db_config, target_db, "deputy_special_warnings", _get_warnings_chunk)

    log.debug("insert_deputy_person_warning")
    transformer(db_config, target_db, "person_warning", get_deputy_person_warning_records)


if __name__ == "__main__":

    runner()
