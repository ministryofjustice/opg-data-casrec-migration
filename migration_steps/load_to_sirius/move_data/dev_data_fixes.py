import logging
import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")
from helpers import format_error_message
from sqlalchemy.sql import text

log = logging.getLogger("root")


def amend_dev_data(db_engine):
    log.info(
        "Amending Dev Sirius DB to match preprod - this should NOT run on preprod!"
    )
    dirname = os.path.dirname(__file__)
    filename = "dev_data_fixes.sql"

    with open(os.path.join(dirname, filename)) as sql_file:
        sql = text(sql_file.read())

    try:

        db_engine.execute(sql)

    except Exception as e:

        log.error(
            f"Unable to amend Sirius DB: data probably already exists",
            extra={
                "file_name": "",
                "error": format_error_message(e=e),
            },
        )
