import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")


import pytest
import logging
import time
from config import get_config
from dotenv import load_dotenv


# set config
current_path = Path(os.path.dirname(os.path.realpath(__file__)))
env_path = current_path / "../.env"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
config = get_config(env=environment)

# logging
log = logging.getLogger("root")


def run_data_tests(verbosity=0):
    t = time.process_time()

    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    test_path = f'{current_path / "data_tests"}'

    pytest_args = [test_path, "--tb=no", "--disable-warnings", "-r N"]

    if verbosity >= 2:
        pytest_args.insert(0, "-v")
        pytest_args.insert(1, "-s")

    log.info(f"Running data tests on {config.SAMPLE_PERCENTAGE}% of data")
    exit_code = pytest.main(pytest_args)

    if exit_code == 0:
        log.info("all tests passed")
    else:
        log.info("tests failed")

    print(f"Total test time: {round(time.process_time() - t, 2)}")
