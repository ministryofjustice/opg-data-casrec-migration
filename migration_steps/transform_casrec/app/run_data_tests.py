import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")


import pytest
import logging
import time
import helpers
from dotenv import load_dotenv
from helpers import log_title


# set config
current_path = Path(os.path.dirname(os.path.realpath(__file__)))
env_path = current_path / "../.env"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)

# logging
log = logging.getLogger("root")


def run_data_tests(verbosity_level="INFO"):
    t = time.process_time()

    log.info(log_title(message="Migration Step: Test Transformed Casrec Data"))
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    test_path = f'{current_path / "data_tests"}'

    pytest_args = [test_path, """--disable-warnings""", """-r N"""]

    if verbosity_level == "INFO":
        pytest_args += ["--tb=line"]
    else:
        pytest_args += ["--tb=long", "-v", "-s"]

    log.info(
        f"Running data tests on {config.SAMPLE_PERCENTAGE}% of data with at "
        f"least {config.MIN_PERCENTAGE_FIELDS_TESTED}% of fields tested"
    )
    exit_code = pytest.main(pytest_args)

    if exit_code == 0:
        log.info("All tests passed")
    else:
        log.error("Tests failed")

    log.info(f"Total test time: {round(time.process_time() - t, 2)}")
