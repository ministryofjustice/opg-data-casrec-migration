import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import time
from config import get_config
from dotenv import load_dotenv
from helpers import *
import logging
import custom_logger
import click
import boto3

env_path = current_path / "../../../../.env"
sql_path = current_path / "sql"
csv_path = current_path / "csvs"
responses_path = current_path / "responses"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
config = get_config(environment)

session = boto3.session.Session()
host = os.environ.get("DB_HOST")
ci = os.getenv("CI")
account = os.environ["SIRIUS_ACCOUNT"]
account_name = os.environ.get("ACCOUNT_NAME")
bucket_name = f"casrec-migration-{account_name.lower()}"


# logging
log = logging.getLogger("root")
custom_logger.setup_logging(env=environment, module_name="upload api test data")


@click.command()
@click.option("-v", "--verbose", count=True)
def main(verbose):
    # set_logging_level(verbose)
    log.info(log_title(message="API CSV Upload"))

    log.info("Perform Upload to S3 for API files")
    log.info("Adding csv and response files to bucket...\n")

    s3 = get_s3_session(session, environment, host, ci=ci, account=account)

    paths = ["validation/responses", "validation/csvs"]
    for path in paths:
        for file in os.listdir(current_path / path):
            file_path = f"{current_path}/{path}/{file}"
            s3_file_path = f"{path}/{file}"
            if file.endswith(".json") or file.endswith(".csv"):
                upload_file(bucket_name, file_path, s3, log, s3_file_path)

    # uncomment for troubleshooting
    # s3_files = get_list_of_s3_files(bucket_name, s3, paths)


if __name__ == "__main__":
    t = time.process_time()

    log.setLevel(1)
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
