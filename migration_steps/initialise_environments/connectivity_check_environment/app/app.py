import sys
import os
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

from sqlalchemy import create_engine
from botocore.exceptions import ClientError
import custom_logger
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

# Config
config = get_config(environment)

# logging
custom_logger.setup_logging(
    env=environment, module_name="configuration check", level="INFO"
)
log = logging.getLogger("root")

# DB
# load_casrec_engine = create_engine(config.get_db_connection_string("casrec"))
migration_engine = create_engine(config.get_db_connection_string("migration"))
sirius_engine = create_engine(config.get_db_connection_string("target"))

# S3
s3_url = os.environ.get("S3_URL")
s3 = get_s3_session(environment, s3_url, ci=ci, account=account)
bucket_name = f"casrec-migration-{account_name.lower()}"


def add_test_item_to_bucket(s3, bucket_name):
    fname = "test_file.txt"
    f = open(fname, "a")
    f.write("This is a test file!")
    f.close()

    log.info(f"Put test file in root of {bucket_name}")

    try:
        upload_file(bucket_name, f"{fname}", s3, log, "validation/api_tests/test.txt")
    except ClientError as e:
        logging.error(e)
        return False

    # resp = s3.list_objects_v2(Bucket=bucket_name, Prefix=f"{path}/")


print(environment)
add_test_item_to_bucket(s3, bucket_name)


# -- put something in each s3 folder
# -- remove test file from each s3 folder
# -- connect to database and select count from load
# -- connect to database and select count from source
# -- connect to database and select count from target
# -- check for 200 response from frontend
