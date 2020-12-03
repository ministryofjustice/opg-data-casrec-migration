import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../migration_steps/shared")

from migration_steps.load_to_target.app.entities.client import target_update


def test_target_update(caplog, test_config, mock_df_from_sql_file, mock_execute_update):

    config = test_config

    target_update(config=config, conn_migration="fake_db_1", conn_target="fake_db_2")

    print(f"caplog.text: {caplog.text}")
    assert "cols: ['firstname', 'surname']" in caplog.text
    assert "pk_col: id" in caplog.text
