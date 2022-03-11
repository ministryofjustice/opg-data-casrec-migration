"""
Apply post-migration fixes in order to a local Sirius db.
This should be run after bringing Sirius up and performing
a full successful migrate.sh run against it.
"""
import os
import re
from glob import glob

import sqlalchemy


user = os.environ.get("DB_USER", "api")
password = os.environ.get("DB_PASSWORD", "api")
host = os.environ.get("DB_HOST", "localhost")
port = os.environ.get("DB_PORT", 5432)
dbname = os.environ.get("DB_NAME", "api")


conn_str = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
engine = sqlalchemy.create_engine(conn_str, echo=True)


"""
Run all the post migration scripts in folders prefixed with two digits;
for the purposes of ordering, each post-migration script should be within a numbered folder
in format XX_pmf_*; within each folder, if the scripts need to run in a specific order, they
should also be prefixed with two digits to signify the ordering.
"""
sql_scripts = glob(os.path.join(os.path.dirname(__file__), "./**/*.sql"))
sql_scripts = list(
    filter(
        lambda script_path: re.search(r"[\d]{2}_pmf", script_path) is not None,
        sql_scripts,
    )
)
sql_scripts = sorted(sql_scripts)


with engine.begin() as conn:
    for script_path in sql_scripts:
        with open(script_path, "r") as script:
            sql = script.read().replace("ROLLBACK;", "")
            conn.execute(sqlalchemy.text(sql))
