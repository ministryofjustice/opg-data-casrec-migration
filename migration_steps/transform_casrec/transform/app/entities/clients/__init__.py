import logging
import pandas as pd

from entities.clients.addresses import get_addresses_clients_chunk
from entities.clients.person_caseitem import get_person_caseitem_records
from entities.clients.persons import get_client_persons_chunk
from entities.clients.phonenumbers import get_phonenumbers_clients_chunk
from helpers import log_title, check_entity_enabled
from transform_data.transformer import transformer


log = logging.getLogger("root")

# shared function which does a select across the whole persons table;
# returns a dict with a 'persons_df' key which can be referenced in chunk functions
# called from migrator()
def _do_persons_prep(db_config, target_db, mapping_file_name):
    # look up from the persons table once, and use resulting df for each chunk
    persons_query = (
        f'select "id", "caserecnumber" as "c_caserecnumber" from {db_config["target_schema"]}.persons '
        f"where \"type\" = 'actor_client';"
    )

    return {
        'persons_df': pd.read_sql_query(persons_query, db_config["db_connection_string"])
    }

def runner(target_db, db_config):
    """
    | Name      | Running Order | Requires |
    | --------- | ------------- | -------- |
    | persons   | 1             |          |
    | addresses | 2             | persons  |
    |           |               |          |

    """

    entity_name = "clients"
    extra_entities = ["cases", "deputies"]
    if not check_entity_enabled(entity_name, extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_client_persons")
    transformer(db_config, target_db, "client_persons", get_client_persons_chunk)

    log.debug("insert_addresses_clients")
    transformer(db_config, target_db, "client_addresses", get_addresses_clients_chunk, _do_persons_prep)

    log.debug("insert_phonenumbers_clients")
    transformer(db_config, target_db, "client_phonenumbers", get_phonenumbers_clients_chunk, _do_persons_prep)

    log.debug("insert_person_caseitem")
    transformer(db_config, target_db, "person_caseitem", get_person_caseitem_records, _do_persons_prep)


if __name__ == "__main__":

    runner()
