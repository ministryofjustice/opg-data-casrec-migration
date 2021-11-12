import logging
import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")
from helpers import format_error_message
from sqlalchemy.sql import text

log = logging.getLogger("root")


def amend_dev_assignees(db_engine):
    assignee_ids = [2657]
    assignee_ids.extend(range(2, 510))
    team_ids = [
        90,
        91,
        92,
        93,
        94,
        95,
        96,
        97,
        98,
        99,
        100,
        101,
        102,
        103,
        104,
        109,
        119,
        141,
        193,
        229,
        266,
        267,
        268,
        279,
        285,
        380,
        381,
        382,
        383,
        384,
        415,
        465,
        479,
        480,
    ]
    teams = [f"({team_id}, 'Migration Team', 'assignee_team')" for team_id in team_ids]
    users = [
        f"({user_id}, 'Migration User', 'assignee_user')"
        for user_id in assignee_ids
        if user_id not in team_ids
    ]
    assignees = teams + users

    sql = f"""
        INSERT INTO public.assignees (id, name, type)
        VALUES {",".join(assignees)}
        ON CONFLICT (id) DO UPDATE
            SET name = excluded.name,
                type = excluded.type;
    """

    try:
        db_engine.execute(sql)

    except Exception as e:
        log.error(
            f"Unable to insert/update assignees in Sirius DB",
            extra={
                "error": format_error_message(e=e),
            },
        )


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
        print(f"e: {e}")
        log.error(
            f"Unable to amend Sirius DB: data probably already exists",
            extra={
                "file_name": "",
                "error": format_error_message(e=e),
            },
        )

    amend_dev_assignees(db_engine=db_engine)
