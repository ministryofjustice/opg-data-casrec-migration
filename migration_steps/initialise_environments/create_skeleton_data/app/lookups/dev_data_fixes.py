import logging
import os
import sys
from pathlib import Path
from helpers import get_lookup_dict

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")
from helpers import format_error_message
from sqlalchemy.sql import text

log = logging.getLogger("root")


def amend_dev_assignees(db_engine):
    assignee_ids = [2657]
    lookup_dict = get_lookup_dict(file_name="caseowner_lookup")
    lookup_ids = list(lookup_dict.values())

    # We have a couple of casrec users mapping to the same assignee. Remove duplicates
    lookup_ids = list(dict.fromkeys(lookup_ids))

    assignee_ids.extend(sorted(lookup_ids))
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
    teams = [
        f"({team_id}, 'Migration Team {team_id}', 'assignee_team', 'ALLOCATIONS')"
        for team_id in team_ids
    ]
    users = [
        f"({user_id}, 'Migration User', 'assignee_user', null)"
        for user_id in assignee_ids
        if user_id not in team_ids
    ]
    assignees = teams + users

    # assign all users to team ID 100, for dev testing purposes
    user_teams = [
        f"(100, {user_id})" for user_id in assignee_ids if user_id not in team_ids
    ]

    sql = f"""
        INSERT INTO public.assignees (id, name, type, teamtype)
        VALUES {",".join(assignees)}
        ON CONFLICT (id) DO UPDATE
            SET name = excluded.name,
                type = excluded.type,
                teamtype = excluded.teamtype;

        INSERT INTO assignee_teams (team_id, assignablecomposite_id)
        VALUES {",".join(user_teams)}
        ON CONFLICT ON CONSTRAINT assignee_teams_pkey DO NOTHING;
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
    amend_dev_assignees(db_engine=db_engine)
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
