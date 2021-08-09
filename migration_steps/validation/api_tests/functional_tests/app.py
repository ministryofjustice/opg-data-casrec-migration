import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")
sys.path.append(str(current_path) + "/../shared")
sys.path.append(str(current_path))
# logging
environment = os.environ.get("ENVIRONMENT")
# Update to DEBUG for extra logging whilst developing
from api_test import ApiTests


def get_post_data(entity):
    post_data = {
        "warnings": {
            "data": {
                "warningText": "<p>Blah<\/p>",
                "warningType": {
                    "handle": "REM - Violence Warnings",
                    "label": "REM - Violence Warnings",
                },
            },
            "url": "clients/{id}/warnings",
            "case_references": ["10194709"],
        },
        "bonds": {
            "data": {
                "bond": {
                    "requiredBondAmount": "1000",
                    "amountTaken": "500",
                    "bondProviderId": "186",
                    "companyName": "Random",
                    "referenceNumber": "RND12345",
                    "oneOff": False,
                    "renewalDate": "19/03/2018",
                },
                "securityBond": True,
            },
            "url": "/orders/{id}/bonds",
            "case_references": ["10001403"],
        },
    }

    try:
        return_object = post_data[entity]
    except Exception:
        return_object = None

    return return_object


def get_put_data(entity):
    put_data = {}

    try:
        return_object = put_data[entity]
    except Exception:
        return_object = None

    return return_object


def get_get_data(entity):
    get_data = {}

    try:
        return_object = get_data[entity]
    except Exception:
        return_object = None

    return return_object


def main():
    entities = [
        "warnings",
    ]

    api_tests = ApiTests()
    api_tests.create_a_session()

    for entity in entities:
        data = {
            "post_objects": get_post_data(entity),
            "put_objects": get_put_data(entity),
            "delete_objects": get_get_data(entity),
        }
        api_tests.run_functional_test(entity, data)


if __name__ == "__main__":
    main()
