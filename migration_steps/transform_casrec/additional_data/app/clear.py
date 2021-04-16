import logging

import datetime
import json
import os
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")
from helpers import get_additional_data_dict


log = logging.getLogger("root")


def clear_tables(db_config, files):
    for additional_data_file_name in files:
        additional_data_dict = get_additional_data_dict(
            file_name=additional_data_file_name
        )
        additional_data_table_name = f"additional_data_{additional_data_dict['entity']}_{additional_data_dict['sirius_table']}"

        target_db_engine = create_engine(db_config["db_connection_string"])

        try:

            with target_db_engine.begin() as conn:

                conn.execute(
                    f"DROP TABLE IF EXISTS {db_config['target_schema']}.{additional_data_table_name};"
                )
                log.debug(f"dropped table '{additional_data_table_name}'")

        except Exception as e:
            log.error(f"TERRIBLE ERROROR dropping table {additional_data_table_name}")
            print(f"e: {e}")
