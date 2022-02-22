import sys
import os
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

from sqlalchemy import create_engine

from botocore.exceptions import ClientError
import custom_logger
import requests
import time
from dotenv import load_dotenv
from helpers import get_config, log_title, get_s3_session, upload_file
import logging

env_path = current_path / "../../../.env"
load_dotenv(dotenv_path=env_path)

# Env variables
ci = os.getenv("CI")
account = os.environ.get("SIRIUS_ACCOUNT")
path = os.environ.get("S3_PATH")
environment = os.environ.get("ENVIRONMENT")
account_name = os.environ.get("ACCOUNT_NAME")
base_url = os.environ.get("SIRIUS_FRONT_URL")

# Config
config = get_config(environment)

# logging
custom_logger.setup_logging(
    env=environment, module_name="configuration check", level="INFO"
)
log = logging.getLogger("root")

# DB
if environment != "local":
    load_casrec_engine = create_engine(config.get_db_connection_string("casrec"))
expected_load_db = config.db_config["casrec"]["name"]
migration_engine = create_engine(config.get_db_connection_string("migration"))
expected_migration_db = config.db_config["migration"]["name"]
sirius_engine = create_engine(config.get_db_connection_string("target"))
expected_sirius_db = config.db_config["target"]["name"]

# S3
s3_url = os.environ.get("S3_URL")
s3 = get_s3_session(environment, s3_url, ci=ci, account=account)
bucket_name = f"casrec-migration-{account_name.lower()}"
test_text = "This is a test file!"


def add_test_item_to_bucket(s3, bucket_name):
    fname = "test_file.txt"
    f = open(fname, "w")
    f.write(test_text)
    f.close()

    log.info(f"Adding test file in root of {bucket_name}")

    try:
        upload_file(bucket_name, f"{fname}", s3, log, "validation/logs/test_log.log")
        upload_file(
            bucket_name, f"{fname}", s3, log, "validation/report/test_report.txt"
        )
        log.info(f"Test file added successfully to {bucket_name}")
    except ClientError as e:
        logging.error(e)
        return False


def pull_from_bucket(s3, bucket_name):
    path = "validation/report"
    file = f"{path}/test_report.txt"
    log.info("Attempting to list files..")
    try:
        resp = s3.list_objects_v2(Bucket=bucket_name, Prefix=f"{path}/")
        if "Contents" not in resp:
            log.error(
                f"ERROR no files found - please check you have added files to {path}"
            )
            os._exit(1)
        log.info("Files listed successfully..")
    except Exception:
        log.error("Cannot list objects in bucket")
    log.info("Attempting to get file..")
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=file)
        text = obj["Body"].read()
        assert text.decode("utf-8") == test_text, log.error("File contents incorrect")
        log.info("File downloaded successfully..")
    except Exception:
        log.error(f"Unable to get file: {file}")


def check_db_connectivity(engine, expected_db_name):
    sql = "SELECT current_database();"
    log.info(f"Connecting to {expected_db_name}")
    try:
        sql_response = engine.execute(sql)
        db_name = sql_response.one()._mapping["current_database"]
        assert db_name == expected_db_name, log.error("DB name incorrect")
        log.info(f"Successfully Connected to {expected_db_name}")
    except Exception:
        log.error(f"Could not connect to DB {expected_db_name}")


def check_sirius_fe_connectivity():
    log.info(f"Connecting to Sirius frontend")
    try:
        response = requests.get(base_url)
        assert response.status_code in (200, 401), log.error(
            f"Response from frontend: {response.status_code}"
        )
        log.info(f"Successfully Connected to Sirius frontend")
    except Exception:
        log.error("Unknown connection error to sirius frontend")


def main():
    log.info(f"Running in environment: {environment}")
    add_test_item_to_bucket(s3, bucket_name)
    pull_from_bucket(s3, bucket_name)
    if environment != "local":
        check_db_connectivity(load_casrec_engine, expected_load_db)
    check_db_connectivity(migration_engine, expected_migration_db)
    check_db_connectivity(sirius_engine, expected_sirius_db)
    if environment != "local":
        check_sirius_fe_connectivity()


if __name__ == "__main__":
    t = time.process_time()
    main()
    log.info(f"Total time: {round(time.process_time() - t, 2)}")
