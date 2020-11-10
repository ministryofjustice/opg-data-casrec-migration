import pytest

from config import LocalConfig

from data_tests.clients import cases_clients_persons, cases_clients_addresses

SAMPLE_PERCENTAGE = 1


list_of_test_cases = [cases_clients_persons, cases_clients_addresses]


@pytest.fixture
def get_config(env="local"):
    if env == "local":
        config = LocalConfig()

    return config
