"""
Apply post-migration fixes in order to a local Sirius db.
This should be run after bringing Sirius up and performing
a full successful migrate.sh run against it.
"""
import io
import os
import re
import sys
from glob import glob

import sqlalchemy


CASREC_MAPPING_SCHEMA = "casrec_mapping"

user = os.environ.get("DB_USER", "api")
password = os.environ.get("DB_PASSWORD", "api")
host = os.environ.get("DB_HOST", "localhost")
port = os.environ.get("DB_PORT", 5432)
dbname = os.environ.get("DB_NAME", "api")


conn_str = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
engine = sqlalchemy.create_engine(conn_str, echo=True)


casrec_user = os.environ.get("DB_USER", "casrec")
casrec_password = os.environ.get("DB_PASSWORD", "casrec")
casrec_host = os.environ.get("DB_HOST", "localhost")
casrec_port = os.environ.get("DB_PORT", 6666)
casrec_dbname = os.environ.get("DB_NAME", "casrecmigration")

casrec_conn_str = f"postgresql://{casrec_user}:{casrec_password}@{casrec_host}:{casrec_port}/{casrec_dbname}"
casrec_engine = sqlalchemy.create_engine(casrec_conn_str, echo=True)


# cribbed from
# https://www.pythonsheets.com/notes/python-sqlalchemy.html#fastest-bulk-insert-in-postgresql-via-copy-statement
# create_sql: SQL to create destination table in the casrec_mapping schema (include schema name in CREATE)
# from_sql: SQL to select records to be inserted into destination table (usually from integration schema)
# to_table: destination table in casrec_mapping schema (fully qualified name)
def _copy(create_sql, from_sql, to_table):
    # Export the data from casrec table(s)
    datafile = io.StringIO()

    casrec_raw_conn = casrec_engine.raw_connection()
    with casrec_raw_conn.cursor() as cur:
        cur.copy_expert(
            f"COPY ({sqlalchemy.text(from_sql)}) TO STDOUT WITH CSV HEADER", datafile
        )

    datafile.seek(0)

    # Set up destination table
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text(create_sql))
        conn.execute(f"TRUNCATE {to_table}")

    # Import data into casrec_mapping table
    raw_conn = engine.raw_connection()
    with raw_conn.cursor() as cur:
        cur.copy_expert(f"COPY {to_table} FROM STDIN CSV HEADER", datafile)
    raw_conn.commit()


def _run_sql_scripts(sql_scripts):
    with engine.begin() as conn:
        for script_path in sql_scripts:
            with open(script_path, "r") as script:
                sql = script.read().replace("ROLLBACK;", "")
                conn.execute(sqlalchemy.text(sql))


"""
Mapping tables. This is idempotent, so we do it every time this script runs.
"""
with engine.begin() as conn:
    conn.execute(f"CREATE SCHEMA IF NOT EXISTS {CASREC_MAPPING_SCHEMA};")

# Mapping from Sirius case ID to casrec Order No
_copy(
    f"""
    CREATE TABLE IF NOT EXISTS {CASREC_MAPPING_SCHEMA}.cases (
        sirius_id int,
        "Order No" varchar
    )
    """,
    'SELECT id AS sirius_id, c_order_no AS "Order No" FROM integration.cases',
    f"{CASREC_MAPPING_SCHEMA}.cases",
)

# Mapping from Sirius annual_report_type_assignments ID to migrated reporttype and type
_copy(
    f"""
    CREATE TABLE IF NOT EXISTS {CASREC_MAPPING_SCHEMA}.annual_report_type_assignments (
        sirius_id int PRIMARY KEY,
        reporttype varchar,
        type varchar
    )
    """,
    "SELECT id AS sirius_id, reporttype, type FROM integration.annual_report_type_assignments",
    f"{CASREC_MAPPING_SCHEMA}.annual_report_type_assignments",
)

# Mapping from Sirius annual_report_logs ID to migrated status
_copy(
    f"""
    CREATE TABLE IF NOT EXISTS {CASREC_MAPPING_SCHEMA}.annual_report_logs (
        sirius_id int PRIMARY KEY,
        status varchar
    )
    """,
    "SELECT id AS sirius_id, status FROM integration.annual_report_logs",
    f"{CASREC_MAPPING_SCHEMA}.annual_report_logs",
)


if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
    # run a single script
    _run_sql_scripts([sys.argv[1]])
else:
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

    _run_sql_scripts(sql_scripts)
