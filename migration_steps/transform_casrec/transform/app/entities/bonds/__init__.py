import logging
import pandas as pd

from entities.bonds.bonds_active import get_bonds_active_chunk
from entities.bonds.bonds_dispensed import get_bonds_dispensed_chunk
from helpers import log_title, check_entity_enabled
from transform_data.transformer import transformer


log = logging.getLogger("root")

def _do_existing_cases_prep(db_config, target_db, mapping_file_name):
    existing_cases_query = f"SELECT c_cop_case, c_bond_no, id from {db_config['target_schema']}.cases;"

    return {
        'existing_cases_df': pd.read_sql_query(existing_cases_query, db_config["db_connection_string"])
    }

def runner(target_db, db_config):
    """
    | Name      | Running Order | Requires |
    | --------- | ------------- | -------- |
    | bonds   | 1               | cases    |
    |           |               |          |
    |           |               |          |

    """

    entity_name = "bonds"
    extra_entities = ["cases"]
    if not check_entity_enabled(entity_name=entity_name, extra_entities=extra_entities):
        return False

    log.info(log_title(message=entity_name))

    log.debug("insert_bonds_active")
    transformer(db_config, target_db, "bonds_active", get_bonds_active_chunk, _do_existing_cases_prep)

    log.debug("insert_bonds_dispensed")
    transformer(db_config, target_db, "bonds_dispensed", get_bonds_dispensed_chunk, _do_existing_cases_prep)

if __name__ == "__main__":

    runner()
