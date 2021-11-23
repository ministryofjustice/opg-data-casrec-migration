import os
import sys
from io import StringIO

import pandas as pd
from pandas.testing import assert_frame_equal
from sqlalchemy import create_engine

current_path = os.path.dirname(__file__)
transform_app_path = os.path.join(
    current_path, "..", "..", "migration_steps", "transform_casrec", "transform", "app"
)
shared_path = os.path.join(current_path, "..", "..", "migration_steps", "shared")

sys.path.insert(0, transform_app_path)
sys.path.insert(0, shared_path)

from db_insert import InsertData
from helpers import get_table_def
from utilities.clear_database import clear_tables

# THIS IS WHAT WE'RE TESTING
from entities.reporting.annual_report_type_assignments import (
    insert_annual_report_type_assignments,
)

# TODO get connection string from config
DB_CONFIG = {
    "db_connection_string": "postgresql://casrec:casrec@localhost:6666/casrecmigration",  # pragma: allowlist secret
    "source_schema": "test_casrec",
    "target_schema": "test_transform",
    "chunk_size": 1,
}

# TEST CASES PUT DATA INTO BOTH THE CASREC DB STAND-IN AND THE TRANSFORM DB
# this is because some transforms rely on both, re-using the outputs of
# previous transforms
TRANSFORM_UNDER_TEST = insert_annual_report_type_assignments

MAPPING_FILE = "annual_report_type_assignments"

TEST_CASES = [
    {
        "source_data": [
            {
                "table": "order",
                "records": {
                    "Ord Stat": ["Active", "Closed", "Active"],
                    "Ord Risk Lvl": ["3", "2", "2"],
                    "Case": ["C1", "C2", "C2"],
                },
            }
        ],
        "target_data": [
            {
                "table": "annual_report_logs",
                "records": {"id": [1, 2], "c_case": ["C1", "C2"]},
            }
        ],
        "expected_data": {
            "reporttype": ["OPG103", "OPG102"],
            "type": ["-", "-"],
            "annualreport_id": [1, 2],
        },
    }
]

# !!!!!! TEST CODE STARTS HERE - should be able to pass configuration to a function/object
# to do all of the below

db_engine = create_engine(DB_CONFIG["db_connection_string"])

# TARGET DB STAND-IN
target_db = InsertData(db_engine=db_engine, schema=DB_CONFIG["target_schema"])

# SOURCE (CASREC) DB STAND-IN
source_db = InsertData(db_engine=db_engine, schema=DB_CONFIG["source_schema"])

# ooh, naughty, pretending source schema is target schema so clear_tables() works...
source_config = DB_CONFIG.copy()
source_config.update({"target_schema": DB_CONFIG["source_schema"]})

dest_table_for_transform = get_table_def(mapping_name=MAPPING_FILE)[
    "destination_table_name"
]

for test_case in TEST_CASES:
    # CLEAR TABLES
    clear_tables(db_config=DB_CONFIG)
    clear_tables(db_config=source_config)

    # SET UP SOURCE
    # insert test data into source db (represents source for current transform if required)
    for source_data_for_table in test_case["source_data"]:
        table_name = source_data_for_table["table"]
        records = source_data_for_table["records"]
        source_db.insert_data(
            pd.DataFrame(records), table_name=table_name, sirius_details={}
        )

    # SET UP TARGET
    # insert test data into target db (represents previous transforms)
    for target_data_for_table in test_case["target_data"]:
        table_name = target_data_for_table["table"]
        records = target_data_for_table["records"]
        target_db.insert_data(
            pd.DataFrame(records), table_name=table_name, sirius_details={}
        )

    # APPLY TRANSFORM
    TRANSFORM_UNDER_TEST(
        mapping_file=MAPPING_FILE,
        target_db=target_db,
        db_config=DB_CONFIG,
    )

    # CHECK RESULTING TARGET TABLE
    expected_df = pd.DataFrame(test_case["expected_data"])

    # query from the table that the transform inserts data into
    actual_df = pd.read_sql_query(
        f'SELECT * FROM {DB_CONFIG["target_schema"]}.{dest_table_for_transform}',
        DB_CONFIG["db_connection_string"],
    )

    # drop id and casrec_details columns, as we won't use these for comparison
    actual_df = actual_df.drop(columns=["id", "casrec_details"])

    # compare the expected dataframe with the actual dataframe
    assert_frame_equal(expected_df, actual_df)
