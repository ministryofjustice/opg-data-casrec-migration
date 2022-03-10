import json
import logging
import os
import psycopg2
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../../shared")

from helpers import get_config

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")
config = get_config(environment)


def generate_letters(conn_target, target_schema):
    cursor = conn_target.cursor()

    with open(current_path / "sql/schema_reset.sql", "r") as file:
        sql = file.read()

    cursor.execute(sql)

    sirius_dates = json.load(open(current_path / "sirius_dates.json"))
    for date, params in sirius_dates.items():
        generate_letters_for_date(cursor, date, params, target_schema)

    cursor.close()
    conn_target.commit()


def generate_letters_for_date(cursor, date, params, target_schema):
    with open(current_path / "sql/sirius_letters.sql", "r") as file:
        sql = file.read()

    sql = sql.replace("{letter_date}", f"'{date}'")
    sql = sql.replace("{target_schema}", target_schema)
    sql = sql.replace("{clientsource}", config.migration_phase)

    for param, value in params.items():
        sql = sql.replace("{" + param + "}", f"'{value}'")

    cursor.execute(sql)
