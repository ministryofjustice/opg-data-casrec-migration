import logging
import os
import sys
from pathlib import Path

import pandas as pd

from utilities.db_helpers import generate_select_query

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../../shared")

from db_insert import InsertData

log = logging.getLogger("root")


def copy_tables(db_config, source_db_engine, target_db_engine, tables):
    target_db = InsertData(
        db_engine=target_db_engine,
        schema=db_config["target_schema"],
        empty_string_to_null=False,
    )

    for table, data in tables.items():
        cols = data.keys()
        log.info(f"Copying {table} ({', '.join(cols)}) from Sirius to Staging")

        source_data_query = generate_select_query(
            schema=db_config["sirius_schema"], table=table, columns=cols, order_by=None
        )
        source_data_df = pd.read_sql_query(con=source_db_engine, sql=source_data_query)

        target_db.insert_data(source_data_df, table, data)
