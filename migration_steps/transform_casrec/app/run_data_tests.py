import logging
import os
import time
from pathlib import Path
import get_shared_utilities
import pytest
from config import get_config
from dotenv import load_dotenv
from pytest import ExitCode


current_path = Path(os.path.dirname(os.path.realpath(__file__)))
env_path = current_path / "../.env"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
config = get_config(env=environment)

log = logging.getLogger("root")


def pytest_addoption(parser):
    parser.addoption("--additional_arguments", action="store", help="some helptext")


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
