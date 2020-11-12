import json
import os

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


def add_to_tested_list(module_name, tested_fields):
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, f"./field_list")
    file_name = "tested_fields.json"

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    try:
        with open(f"{file_path}/{file_name}", "r") as fields_json:
            fields_dict = json.load(fields_json)
    except IOError:
        fields_dict = {}
    try:
        field_list = list(set(fields_dict[module_name]) | set(tested_fields))
        fields_dict[module_name] = field_list
    except KeyError:
        fields_dict[module_name] = tested_fields

    with open(f"{file_path}/{file_name}", "w") as json_out:
        json.dump(fields_dict, json_out, indent=4)


def pytest_sessionfinish(session):
    print("Session finish, deleting field tracker files")

    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, f"./field_list")
    file_name = "tested_fields.json"
    os.remove(f"{file_path}/{file_name}")
