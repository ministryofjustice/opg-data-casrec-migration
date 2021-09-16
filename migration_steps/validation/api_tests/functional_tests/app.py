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
        "warnings": [
            {
                "title": "Create New Warnings",
                "data": {
                    "warningText": "<p>Blah<\/p>",
                    "warningType": {
                        "handle": "REM - Violence Warnings",
                        "label": "REM - Violence Warnings",
                    },
                },
                "url": "clients/{id}/warnings",
                "expected_status": 201,
                "source": "clients",
                "case_references": ["10194709"],
            },
        ],
        # "death": [
        #     {
        #         "title": "Create New Death",
        #         "data": {
        #             "proofOfDeathReceived": True,
        #             "dateLetterSentOut": "",
        #             "dateOfDeath": "09/08/2021",
        #             "dateDeathCertificateReceived": "",
        #             "dateNotified": "09/08/2021",
        #             "notifiedBy": {
        #               "handle": "DEPUTY",
        #               "label": "Deputy"
        #             },
        #             "notifiedByOther": "",
        #             "notificationMethod": "Phone",
        #             "notes": ""
        #         },
        #         "url":             "persons/{id}/death-notification",
        #         "expected_status": 201,
        #         "source":          "clients",
        #         "case_references": ["10138356"],
        #     }
        # ],
        "supervision": [
            {
                "title": "Create Supervision",
                "data": {
                    "notes": "",
                    "appliesFrom": "02/08/2021",
                    "newLevel": "MINIMAL",
                    "newAssetLevel": "LOW",
                },
                "url": "orders/{id}/supervision-level",
                "expected_status": 200,
                "source": "orders",
                "case_references": ["10001668"],
            }
        ],
        "orders": [
            {
                "title": "Create New Orders",
                "data": {
                    "caseSubtype": "PFA",
                    "orderSubtype": {"handle": "TRUSTEE", "label": "Trustee"},
                    "caseRecNumber": "10013583",
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
                "case_references": ["10013583"],
            }
        ],
        "visits": [
            {
                "title": "Create New Orders",
                "data": {
                    "visitType": {"handle": "VT-SUP", "label": "Supervision"},
                    "visitSubType": {"handle": "VST-PA", "label": "PA Visit"},
                    "visitUrgency": {"handle": "VU-STAN", "label": "Standard"},
                    "visitDueDate": "01/01/2021",
                },
                "url": "clients/{id}/visits",
                "expected_status": 201,
                "source": "clients",
                "case_references": ["10013583"],
            }
        ],
        "invoice": [
            {
                "title": "Create New Credit Memo On Invoice",
                "data": {
                    "type": "CREDIT MEMO",
                    "amount": "10",
                    "notes": "<p>Adding credit of 10</p>",
                },
                "url": "finance/{id}/invoice/{id2}/ledger-entries",
                "id2_url": "finance/{id}/invoices",
                "id2_json_path": '[0]["id"]',
                "expected_status": 201,
                "source": "clients",
                "case_references": ["10041221", "10162667", "10015105", "10050512"],
            },
            {
                "title": "Create New Write Off On Invoice",
                "data": {
                    "type": "CREDIT WRITE OFF",
                    "amount": 100,
                    "notes": "<p>Write Off</p>",
                },
                "url": "finance/{id}/invoice/{id2}/ledger-entries",
                "id2_url": "finance/{id}/invoices",
                "id2_json_path": '[0]["id"]',
                "expected_status": 201,
                "source": "clients",
                "case_references": ["13547686"],
            },
            {
                "title": "Create New Write Off On Invoice",
                "data": {
                    "type": "CREDIT WRITE OFF",
                    "amount": 320,
                    "notes": "<p>Write Off</p>",
                },
                "url": "finance/{id}/invoice/{id2}/ledger-entries",
                "id2_url": "finance/{id}/invoices",
                "id2_json_path": '[0]["id"]',
                "expected_status": 201,
                "source": "clients",
                "case_references": ["10027832", "94009939"],
            },
            {
                "title": "Create New Write Off On Invoice",
                "data": {
                    "type": "CREDIT WRITE OFF",
                    "amount": 32.9,
                    "notes": "<p>Write Off</p>",
                },
                "url": "finance/{id}/invoice/{id2}/ledger-entries",
                "id2_url": "finance/{id}/invoices",
                "id2_json_path": '[0]["id"]',
                "expected_status": 201,
                "source": "clients",
                "case_references": ["94087154"],
            },
        ],
    }

    try:
        return_object = post_data[entity]
    except Exception:
        return_object = None

    return return_object


def get_put_data(entity):
    put_data = {
        "crec": [
            {
                "title": "Edit a Risk Rating",
                "data": {"riskScore": 4, "notes": "<p>Risky</p>"},
                "url": "clients/{id}/edit/risk-score",
                "expected_status": 200,
                "source": "orders",
                "id2_url": None,
                "id2_json_path": None,
                "case_references": ["10036052"],
            },
        ],
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
                    "caseRecNumber": "10013583",
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
                "case_references": ["10013583"],
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
                "case_references": ["10013583"],
            },
        ],
        "deputies": [
            {
                "title": "Edit a Deputy",
                "data": {
                    "deputyType": {"handle": "PRO", "label": "Professional"},
                    "salutation": "Mr",
                    "firstname": "Bob",
                    "otherNames": "",
                    "surname": "Bobly",
                    "dob": "05/08/1987",
                    "previousNames": "Jennifer",
                    "addressLine1": "Studio 38P",
                    "addressLine2": "Susan pass",
                    "addressLine3": "",
                    "town": "South Damien",
                    "postcode": "RM6 9NQ",
                    "county": "HU5 3ER",
                    "country": "",
                    "organisationName": None,
                    "organisationTeamOrDepartmentName": None,
                    "workPhoneNumber": "0808 157 0028",
                    "mobileNumber": "",
                    "homePhoneNumber": "0808 157 0028",
                    "email": "dharrison@hotmail.com",
                    "isAirmailRequired": True,
                },
                "url": "deputies/{id}",
                "expected_status": 200,
                "source": "orders",
                "id2_url": "orders/{id}",
                "id2_json_path": '["deputies"][0]["deputy"]["id"]',
                "case_references": ["10004257"],
            },
        ],
        "clients": [
            {
                "title": "Edit a Client",
                "data": {
                    "memorablePhrase": None,
                    "medicalCondition": None,
                    "salutation": "Brigadier",
                    "firstname": "Jim",
                    "middlenames": "Jones",
                    "surname": "Warden",
                    "dob": "09/10/1990",
                    "previousNames": "Victoria",
                    "email": None,
                    "caseRecNumber": "10028288",
                    "clientAccommodation": {
                        "handle": "HEALTH SERVICE PATIENT",
                        "label": "Health Service Patient",
                        "deprecated": False,
                    },
                    "maritalStatus": "Single",
                    "correspondenceByPost": True,
                    "correspondenceByEmail": False,
                    "correspondenceByPhone": False,
                    "correspondenceByWelsh": False,
                    "addressLine1": "Studio 97",
                    "addressLine2": "Geraldine trail",
                    "addressLine3": "",
                    "town": "Junehaven",
                    "postcode": "S8 2HD",
                    "county": "E6 3FS",
                    "country": None,
                    "isAirmailRequired": False,
                    "phoneNumber": "01174960999",
                    "interpreterRequired": "No",
                    "specialCorrespondenceRequirements": {
                        "audioTape": False,
                        "largePrint": False,
                        "hearingImpaired": False,
                        "spellingOfNameRequiresCare": False,
                    },
                    "casesManagedAsHybrid": False,
                },
                "url": "clients/{id}",
                "expected_status": 200,
                "source": "clients",
                "id2_url": None,
                "id2_json_path": None,
                "case_references": ["10028288"],
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
                "case_references": ["11866428"],
            }
        ]
    }

    try:
        return_object = delete_data[entity]
    except Exception:
        return_object = None

    return return_object


def main():
    entities = [
        "orders",
        "bonds",
        "warnings",
        "deputies",
        "clients",
        "death",
        "supervision",
        "crec",
        "invoice",
    ]

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
