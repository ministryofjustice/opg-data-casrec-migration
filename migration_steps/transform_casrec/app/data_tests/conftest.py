import json
import os

from data_tests.cases import (
    cases_cases,
    cases_person_caseitem,
)
from data_tests.supervision_level import cases_supervision_level_log
from data_tests.clients import cases_clients_persons
from data_tests.clients import cases_clients_addresses, cases_clients_phonenumbers
import pytest

from run_data_tests import config

SAMPLE_PERCENTAGE = config.SAMPLE_PERCENTAGE


list_of_test_cases = [
    cases_clients_persons,
    cases_clients_addresses,
    cases_clients_phonenumbers,
    cases_cases,
    cases_supervision_level_log,
    cases_person_caseitem,
]


@pytest.fixture
def test_config():
    return config


def add_to_tested_list(module_name, tested_fields):

    dirname = os.path.dirname(__file__)
    file_name = "tested_fields.json"

    try:
        with open(f"{dirname}/{file_name}", "r") as fields_json:
            fields_dict = json.load(fields_json)
    except IOError:
        fields_dict = {}
    try:
        field_list = list(set(fields_dict[module_name]) | set(tested_fields))
        fields_dict[module_name] = field_list
    except KeyError:
        fields_dict[module_name] = tested_fields

    with open(f"{dirname}/{file_name}", "w") as json_out:
        json.dump(fields_dict, json_out, indent=4)


def pytest_sessionfinish():
    dirname = os.path.dirname(__file__)

    file_name = "tested_fields.json"
    os.remove(f"{dirname}/{file_name}")
