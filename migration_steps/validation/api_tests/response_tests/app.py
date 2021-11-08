import os
import sys
from pathlib import Path
import logging

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")
sys.path.append(str(current_path) + "/../shared")
from helpers import check_entity_enabled

# logging
environment = os.environ.get("ENVIRONMENT")
# Update to DEBUG for extra logging whilst developing
from api_test import ApiTests

log = logging.getLogger("root")


def main():
    entities = {
        "clients": [{"csv": "clients", "identifier": "client"},],
        "cases": [{"csv": "orders", "identifier": "order"},],
        "bonds": [{"csv": "bonds", "identifier": "order"},],
        "deputies": [
            {"csv": "deputies", "identifier": "deputy"},
            {"csv": "deputy_clients", "identifier": "deputy"},
            {
                "csv": "deputy_clients_count",
                "identifier": "deputy",
                "assert_on_count": True,
            },
            {"csv": "deputy_orders", "identifier": "order_deputy"},
            {"csv": "deputy_fee_payer", "identifier": "order_deputy"},
        ],
        "supervision_level": [{"csv": "supervision_level", "identifier": "order"},],
        "death": [
            {"csv": "client_death_notifications", "identifier": "client"},
            {
                "csv": "deputy_death_notifications",
                "identifier": "deputy",
                "no_retries": True,
            },
        ],
        "warnings": [
            {"csv": "client_warnings", "identifier": "client", "assert_on_list": True},
            {"csv": "deputy_warnings", "identifier": "deputy", "assert_on_list": True},
        ],
        "crec": [{"csv": "crec", "identifier": "client"},],
        "visits": [{"csv": "visits", "identifier": "client"},],
        "reporting": [{"csv": "reports", "identifier": "client"},],
        "invoice": [
            {"csv": "invoice", "identifier": "client", "assert_on_list": True},
        ],
        # "tasks": [
        #     {
        #         "csv": "tasks",
        #         "identifier": "client",
        #         "assert_on_list": True,
        #         "list_in_field": "tasks"
        #     },
        # ],
    }

    api_tests = ApiTests()
    api_tests.enhance_api_user_permissions()

    for entity, tests in entities.items():
        if not check_entity_enabled(entity):
            log.info(f"Entity {entity} is disabled. Skipping API tests")
            continue
        for test in tests:
            api_tests.create_a_session()
            api_tests.csv = test["csv"]
            api_tests.identifier = test["identifier"]
            api_tests.no_retries = "no_retries" in test and test["no_retries"] is True
            api_tests.assert_on_list = (
                "assert_on_list" in test and test["assert_on_list"] is True
            )
            api_tests.assert_on_count = (
                "assert_on_count" in test and test["assert_on_count"] is True
            )
            if "list_in_field" in test:
                api_tests.list_in_field = test["list_in_field"]
            api_tests.run_response_tests()
    api_tests.upload_log_file()

    if api_tests.failed:
        print("Tests Failed")
        # Changing this whilst we are doing first part of deduplication as expecting failures on pre
        if environment in ["local", "development"]:
            exit(1)
    else:
        print("Tests Passed")


if __name__ == "__main__":
    main()
