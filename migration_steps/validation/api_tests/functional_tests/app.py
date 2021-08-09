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
        # "warnings": [
        #     {
        #         "title": "Create New Warnings",
        #         "data": {
        #             "warningText": "<p>Blah<\/p>",
        #             "warningType": {
        #                 "handle": "REM - Violence Warnings",
        #                 "label": "REM - Violence Warnings",
        #             },
        #         },
        #         "url": "clients/{id}/warnings",
        #         "expected_status": 201,
        #         "source": "clients",
        #         "case_references": ["10194709"],
        #     },
        # ],
        "orders": [
            {
                "title": "Create New Orders",
                "data": {
                    "caseSubtype": "PFA",
                    "orderSubtype": {"handle": "TRUSTEE", "label": "Trustee"},
                    "caseRecNumber": "10006413",
                    "orderDate": "01/01/2021",
                    "orderIssueDate": "",
                    "orderStatus": "",
                    "statusDate": "",
                    "orderExpiryDate": "",
                    "receiptDate": "05/06/2021",
                    "title": "",
                    "fileLocationDescription": "",
                    "fileLocationAddress": {
                        "addressLine1": "",
                        "addressLine2": "",
                        "addressLine3": "",
                        "town": "",
                        "postcode": "",
                        "county": "",
                        "country": "",
                        "isAirmailRequired": False,
                    },
                    "howDeputyAppointed": "",
                    "orderNotes": "",
                    "clauseExpiryDate": "",
                    "bondReferenceNumber": "",
                    "bondValue": 0,
                },
                "url": "clients/{id}/orders",
                "expected_status": 201,
                "source": "clients",
                "case_references": ["10006413"],
            }
        ],
    }

    try:
        return_object = post_data[entity]
    except Exception:
        return_object = None

    return return_object


def get_put_data(entity):
    put_data = {
        "bonds": [
            {
                "title": "Edit a Bond",
                "data": {
                    "requiredBondAmount": "10000",
                    "amountTaken": "10000",
                    "bondProviderId": "185",
                    "companyName": None,
                    "referenceNumber": "W11829",
                    "oneOff": False,
                    "renewalDate": "08/12/2006",
                    "reasonForEditing": {"handle": "KEYING", "label": "Keying error"},
                },
                "url": "orders/{id}/bonds/{id2}",
                "expected_status": 200,
                "source": "orders",
                "id2_url": "orders/{id}",
                "id2_json_path": '["bond"]["id"]',
                "case_references": ["10001668"],
            },
            {
                "title": "Delete (dispense) a Bond",
                "data": {
                    "dischargedDate": "02/02/2021",
                    "dispensedReason": {"handle": "KEYING", "label": "Keying error"},
                },
                "url": "orders/{id}/bonds/{id2}/dispense",
                "expected_status": 200,
                "source": "orders",
                "id2_url": "orders/{id}",
                "id2_json_path": '["bond"]["id"]',
                "case_references": ["10001668"],
            },
        ],
        "orders": [
            {
                "title": "Edit an Order",
                "data": {
                    "caseSubtype": "HW",
                    "orderSubtype": {
                        "handle": "REPLACEMENT",
                        "label": "Replacement",
                        "deprecated": None,
                    },
                    "caseRecNumber": "10007261",
                    "orderDate": "26/05/2011",
                    "orderIssueDate": "28/05/2011",
                    "orderStatus": {
                        "handle": "ACTIVE",
                        "label": "Active",
                        "deprecated": False,
                    },
                    "statusDate": None,
                    "orderExpiryDate": None,
                    "receiptDate": "01/06/2011",
                    "title": None,
                    "fileLocationDescription": None,
                    "fileLocationAddress": {
                        "addressLine1": "",
                        "addressLine2": "",
                        "addressLine3": "",
                        "town": "",
                        "postcode": "",
                        "county": "",
                        "country": "",
                        "isAirmailRequired": False,
                    },
                    "howDeputyAppointed": None,
                    "orderNotes": None,
                    "clauseExpiryDate": None,
                    "bondReferenceNumber": None,
                    "bondValue": None,
                    "securityBond": False,
                },
                "url": "orders/{id}",
                "expected_status": 200,
                "source": "orders",
                "id2_url": None,
                "id2_json_path": None,
                "case_references": ["10007261"],
            },
            {
                "title": "Edit an Order Status",
                "data": {
                    "orderStatus": {
                        "handle": "CLOSED",
                        "label": "Closed",
                        "deprecated": "false",
                    },
                    "orderClosureReason": {
                        "handle": "ORDER REVOKED",
                        "label": "Order revoked",
                        "isSupervised": "1",
                    },
                    "statusDate": "05/08/2021",
                    "statusNotes": "<p>Blah</p>",
                },
                "url": "orders/{id}/status",
                "expected_status": 200,
                "source": "orders",
                "id2_url": None,
                "id2_json_path": None,
                "case_references": ["10194709"],
            },
        ],
    }

    try:
        return_object = put_data[entity]
    except Exception:
        return_object = None

    return return_object


def get_delete_data(entity):
    delete_data = {
        "warnings": [
            {
                "title": "Delete a Warning",
                "data": None,
                "url": "clients/{id}/warnings/{id2}",
                "expected_status": 204,
                "source": "clients",
                "id2_url": "persons/{id}/warnings",
                "id2_json_path": '[0]["id"]',
                "case_references": ["10194709"],
            }
        ]
    }

    try:
        return_object = delete_data[entity]
    except Exception:
        return_object = None

    return return_object


def main():
    entities = ["orders", "bonds", "warnings", "deputies"]

    api_tests = ApiTests()
    api_tests.create_a_session()
    api_tests.enhance_api_user_permissions()

    for entity in entities:
        data = {
            "post_objects": get_post_data(entity),
            "put_objects": get_put_data(entity),
            "delete_objects": get_delete_data(entity),
        }
        api_tests.run_functional_test(entity, data)


if __name__ == "__main__":
    main()
