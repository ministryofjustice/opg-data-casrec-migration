import requests
import json
import pandas as pd
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../migration_steps/shared")
from helpers import get_config, get_s3_session

env_path = current_path / "../../migration_steps/.env"
load_dotenv(dotenv_path=env_path)
print_extra_info = True
base_url = os.environ.get("SIRIUS_FRONT_URL")
password = os.environ.get("API_TEST_PASSWORD")
environment = os.environ.get("ENVIRONMENT")
config = get_config(environment)
db_conn_string = config.get_db_connection_string("target")
engine = create_engine(db_conn_string)

clients_headers = [
    '["clientAccommodation"]["handle"]',
    '["salutation"]',
    '["firstname"]',
    '["surname"]',
]

deputies_headers = [
    '["correspondenceByPost"]',
    '["correspondenceByPhone"]',
    '["correspondenceByEmail"]',
    '["correspondenceByWelsh"]',
    '["specialCorrespondenceRequirements"]["audioTape"]',
    '["specialCorrespondenceRequirements"]["largePrint"]',
    '["specialCorrespondenceRequirements"]["hearingImpaired"]',
    '["specialCorrespondenceRequirements"]["spellingOfNameRequiresCare"]',
    '["deputyStatus"]',
    '["workPhoneNumber"]["id"]',
    '["workPhoneNumber"]["phoneNumber"]',
    '["workPhoneNumber"]["type"]',
    '["workPhoneNumber"]["default"]',
    '["homePhoneNumber"]["id"]',
    '["homePhoneNumber"]["phoneNumber"]',
    '["homePhoneNumber"]["type"]',
    '["homePhoneNumber"]["default"]',
    '["email"]',
    '["dob"]',
    '["dateOfDeath"]',
    '["salutation"]',
    '["firstname"]',
    '["surname"]',
    '["otherNames"]',
    '["addressLine1"]',
    '["addressLine2"]',
    '["addressLine3"]',
    '["town"]',
    '["county"]',
    '["postcode"]',
    '["country"]',
    '["isAirmailRequired"]',
    '["phoneNumber"]',
]

orders_headers = [
    '["client"]["firstname"]',
    '["client"]["surname"]',
    '["client"]["dob"]',
    '["client"]["addressLine1"]',
    '["client"]["postcode"]',
    '["orderDate"]',
    '["orderIssueDate"]',
    '["orderStatus"]["handle"]',
    '["deputies"][0]["deputy"]["firstname"]',
    '["deputies"][0]["deputy"]["surname"]',
    '["orderSubtype"]["handle"]',
    '["orderExpiryDate"]',
]

bonds_headers = [
    '["securityBond"]',
    '["bond"]["requiredBondAmount"]',
    '["bond"]["amountTaken"]',
    '["bond"]["referenceNumber"]',
    '["bond"]["renewalDate"]',
    '["bond"]["dischargeDate"]',
    '["bond"]["companyName"]',
    '["bond"]["status"]["handle"]',
    '["bond"]["bondProvider"]["name"]',
]

supervision_level_headers = [
    '["latestSupervisionLevel"]["appliesFrom"]',
    '["latestSupervisionLevel"]["supervisionLevel"]["handle"]',
    '["latestSupervisionLevel"]["assetLevel"]["handle"]',
    '["latestSupervisionLevel"]["notes"]',
]

warnings_headers = ['["warningType"]', '["warningText"]']

crec_headers = [
    '["riskScore"]',
]

deputy_clients_headers = [
    '["persons"][0]["orders"][0]["deputies"][0]["relationshipToClient"]["label"]'
]

deputy_orders_headers = [
    '["statusOnCaseOverride"]["handle"]',
    '["relationshipToClient"]["handle"]',
]

deputy_client_count = []

visits_headers = [
    '[0]["visitType"]["handle"]',
    '[0]["visitSubType"]["handle"]',
    '[0]["whoToVisit"]',
    '[0]["visitDueDate"]',
    '[0]["visitCreatedDate"]',
    '[0]["visitCancellationReason"]',
    '[0]["visitOutcome"]',
    '[0]["visitCompletedDate"]',
]

reports_headers = [
    '[0]["dueDate"]',
    '[0]["reportingPeriodEndDate"]',
    '[0]["reportingPeriodStartDate"]',
    '[0]["revisedDueDate"]',
    '[0]["status"]["handle"]',
    '[0]["reviewStatus"]["handle"]',
    '[0]["randomReviewDate"]',
]

deputy_death_notifications_headers = [
    '["proofOfDeathReceived"]',
    '["dateDeathCertificateReceived"]',
    '["dateLetterSentOut"]',
    '["notifiedBy"]["handle"]',
    '["notificationMethod"]',
    '["person"]["dateOfDeath"]',
    '["dateNotified"]',
]

client_death_notifications_headers = [
    '["proofOfDeathReceived"]',
    '["dateDeathCertificateReceived"]',
    '["dateLetterSentOut"]',
    '["notifiedBy"]["handle"]',
    '["notificationMethod"]',
    '["person"]["dateOfDeath"]',
    '["dateNotified"]',
]

invoices_headers = [
    '["feeType"]',
    '["reference"]',
    '["raisedDate"]',
    '["amount"]',
    '["amountOutstanding"]',
    '["status"]["handle"]',
    '["sopStatus"]["label"]',
]

orders_updated_cases = [
    '["client"]["firstname"]',
    '["client"]["surname"]',
    '["client"]["dob"]',
    '["client"]["addressLine1"]',
    '["client"]["postcode"]',
    '["orderDate"],["orderIssueDate"]',
    '["orderStatus"]["handle"]',
    '["deputies"][0]["deputy"]["firstname"]',
    '["deputies"][0]["deputy"]["surname"]',
    '["orderSubtype"]["handle"]',
    '["orderExpiryDate"]',
]

deputy_fee_payer_headers = ['["feePayer"]']

csvs = [
    "deputy_fee_payer",
    "clients",
    "orders",
    "bonds",
    "deputies",
    "deputy_fee_payer",
    "deputy_orders",
    "deputy_clients",
    "supervision_level",
    "client_death_notifications",
    "deputy_death_notifications",
    "warnings",
    "crec",
    "visits",
    "reports",
    "invoices",
]

search_headers = [
    "endpoint",
    "entity_ref",
    "test_purpose",
    "full_check",
]

entities_of_type_list = ["warnings", "invoices"]


def get_session(base_url, user, password):
    response = requests.get(base_url)
    cookie = response.headers["Set-Cookie"]
    xsrf = response.headers["X-XSRF-TOKEN"]
    headers_dict = {"Cookie": cookie, "x-xsrf-token": xsrf}
    data = {"email": user, "password": password}
    with requests.Session() as s:
        p = s.post(f"{base_url}/auth/login", data=data, headers=headers_dict)
        print(f"Login returns: {p.status_code}")
        return s, headers_dict, p.status_code


def create_a_session(base_url, password):
    env_users = {
        "local": "case.manager@opgtest.com",
        "development": "case.manager@opgtest.com",
        "preproduction": "opg+siriussmoketest@digital.justice.gov.uk",
        "qa": "opg+siriussmoketest@digital.justice.gov.uk",
        "production": "opg+siriussmoketest@digital.justice.gov.uk",
    }
    user = env_users[environment]
    sess, headers_dict, status_code = get_session(base_url, user, password)
    session = {
        "sess": sess,
        "headers_dict": headers_dict,
        "status_code": status_code,
        "base_url": base_url,
    }

    return session


def get_entity_ids(csv_type, caserecnumber, engine, conn):
    person_id_sql = f"""
        SELECT id
        FROM persons
        WHERE caserecnumber = '{caserecnumber}'
        AND clientsource = 'CASRECMIGRATION'"""

    order_id_sql = f"""
        SELECT c.id
        FROM persons p
        INNER join cases c
        on c.client_id = p.id
        WHERE p.caserecnumber = '{caserecnumber}'
        AND p.clientsource = 'CASRECMIGRATION'
        and c.casetype = 'ORDER'"""

    ids = []

    if csv_type in [
        "clients",
        "client_death_notifications",
        "warnings",
        "crec",
        "visits",
        "reports",
        "invoices",
    ]:
        entity_ids = engine.execute(person_id_sql)
        if entity_ids.rowcount > 1:
            print(f"Too many matching rows for {caserecnumber}")
        elif entity_ids.rowcount < 1:
            print(f"No matching rows for {caserecnumber}")
        else:
            entity_id = entity_ids.one().values()[0]
            ids.append(entity_id)
    elif csv_type in [
        "orders",
        "bonds",
        "supervision_level",
        "deputies",
        "deputy_clients",
        "deputy_orders",
        "deputy_death_notifications",
        "deputy_fee_payer",
    ]:
        entity_ids = engine.execute(order_id_sql)
        if entity_ids.rowcount < 1:
            print(f"No matching rows for {caserecnumber}")
        else:
            for entity_id_row in entity_ids:
                entity_id = entity_id_row.values()[0]
                if csv_type in [
                    "deputies",
                    "deputy_clients",
                    "deputy_death_notifications",
                ]:
                    deputies = get_deputy_entity_ids(entity_id, conn)
                    for deputy in deputies:
                        ids.append(deputy)
                elif csv_type in ["deputy_orders", "deputy_fee_payer"]:
                    deputy_orders = get_deputy_order_entity_ids(entity_id, conn)
                    for deputy_order in deputy_orders:
                        ids.append(deputy_order)
                else:
                    ids.append(entity_id)

    return ids


def rationalise_json_value(v, json_block):
    try:
        response_var = eval(v)
        if response_var is None:
            response_var = ""
        else:
            response_var = str(response_var).replace(",", "")
    except IndexError:
        response_var = ""
        pass
    except KeyError:
        response_var = ""
        pass
    except TypeError:
        response_var = ""
        pass
    return response_var


def restructure_text(col, dedupe):
    col_vals = set(col.split("|")) if dedupe else col.split("|")
    col_restructured = sorted(col_vals)
    col_restructured_text = "|".join(str(e) for e in col_restructured)
    try:
        if col_restructured_text.startswith("|"):
            col_restructured_text = col_restructured_text[1:]
    except Exception:
        pass
    try:
        if col_restructured_text.endswith("|"):
            col_restructured_text = col_restructured_text[:-1]
    except Exception:
        pass
    return col_restructured_text


def get_deputy_entity_ids(entity_id, conn):
    response = conn["sess"].get(
        f'{conn["base_url"]}/api/v1/orders/{entity_id}', headers=conn["headers_dict"],
    )

    response_as_json = json.loads(response.text)
    deputies = response_as_json["deputies"]

    deputy_ids = []
    for deputy in deputies:
        try:
            deputy_id = deputy["deputy"]["id"]
        except Exception:
            deputy_id = ""

        if len(str(deputy_id)) > 0:
            deputy_ids.append(deputy_id)

    return deputy_ids


def get_deputy_order_entity_ids(entity_id, conn):
    response = conn["sess"].get(
        f'{conn["base_url"]}/api/v1/orders/{entity_id}', headers=conn["headers_dict"],
    )

    response_as_json = json.loads(response.text)
    deputies = response_as_json["deputies"]

    order_deputy_ids = []
    for deputy in deputies:
        try:
            deputy_id = deputy["deputy"]["id"]
        except Exception:
            deputy_id = ""

        if len(str(deputy_id)) > 0:
            order_deputy_id = {"order_id": entity_id, "deputy_id": deputy_id}
            order_deputy_ids.append(order_deputy_id)

    return order_deputy_ids


def get_deputy_person_entity_ids(entity_id, conn):
    response = conn["sess"].get(
        f'{conn["base_url"]}/api/v1/clients/{entity_id}/orders',
        headers=conn["headers_dict"],
    )

    response_as_json = json.loads(response.text)
    cases = response_as_json["cases"]
    deputy_ids = []
    for case in cases:
        deputies = case["deputies"]
        for deputy in deputies:
            try:
                deputy_id = deputy["deputy"]["id"]
            except Exception:
                deputy_id = ""

            if len(str(deputy_id)) > 0:
                deputy_ids.append(deputy_id)

    return deputy_ids


def get_endpoint_final(entity_id, endpoint, csv):
    if csv in ["deputy_orders", "deputy_fee_payer"]:
        endpoint_final = (
            str(endpoint)
            .replace("{id1}", str(entity_id["order_id"]))
            .replace("{id2}", str(entity_id["deputy_id"]))
        )
    else:
        endpoint_final = str(endpoint).replace("{id}", str(entity_id))

    print(f"Endpoint: {endpoint_final}")
    return endpoint_final


def generate_csv_headers_line(search_headers, csv):
    header_line = ""
    for search_header in search_headers:
        header_line = header_line + search_header + ","
    for entity_header in eval(f"{csv}_headers"):
        header_line = header_line + entity_header + ","
    header_line = header_line[:-1]
    header_line = header_line + "\n"
    return header_line


def get_response_json(
    sirius_app_session, endpoint_final,
):
    response = sirius_app_session["sess"].get(
        f'{sirius_app_session["base_url"]}{endpoint_final}',
        headers=sirius_app_session["headers_dict"],
    )

    if print_extra_info:
        print(response.text)
        print(response.status_code)

    return json.loads(response.text)


def get_list_of_json_blocks_from_response(csv, response_as_json):
    json_blocks_to_loop_through = []
    if csv in entities_of_type_list:
        for sub_json_block in response_as_json:
            json_blocks_to_loop_through.append(sub_json_block)
    else:
        json_blocks_to_loop_through.append(response_as_json)

    return json_blocks_to_loop_through


def get_line_structure_object_from_json_blocks(
    json_blocks_to_loop_through, row, line_structure, csv
):
    for json_block in json_blocks_to_loop_through:
        for search_header in search_headers:
            row_value_from_input_csv = eval(f'row["{search_header}"]')
            try:
                line_structure[search_header] = (
                    line_structure[search_header] + row_value_from_input_csv + "|"
                )
            except Exception:
                # This handles adding the first occurrence
                line_structure[search_header] = row_value_from_input_csv + "|"
        for json_key in eval(f"{csv}_headers"):
            json_value = f"json_block{json_key}"
            rationalised_json_value = rationalise_json_value(json_value, json_block)
            try:
                line_structure[json_key] = (
                    line_structure[json_key] + rationalised_json_value + "|"
                )
            except Exception:
                # This handles adding the first occurrence
                line_structure[json_key] = rationalised_json_value + "|"

    return line_structure


def deduplicate_and_clean(line_structure, csv):
    all_headers = [
        {"dedupe": False, "headers": eval(f"{csv}_headers")},
        {"dedupe": True, "headers": search_headers},
    ]

    for header_data in all_headers:
        for header in header_data["headers"]:
            try:
                line_structure_header = line_structure[header]
            except KeyError:
                line_structure_header = ""

            col_restruct_text = restructure_text(
                line_structure_header, dedupe=header_data["dedupe"]
            )
            line_structure[header] = col_restruct_text

    return line_structure


def convert_structure_to_line(line_structure):
    line = ""
    for attr, value in line_structure.items():
        line = line + value + ","

    line = line[:-1]
    line = line + "\n"

    return line


def main():
    print(f"You are running this script against: {environment}")

    sirius_app_session = create_a_session(base_url, password)

    for csv in csvs:
        full_header_line = generate_csv_headers_line(search_headers, csv)

        with open(f"responses/{csv}_output.csv", "w") as csv_out_file:
            csv_out_file.write(full_header_line)

        input_csv_data = pd.read_csv(f"{csv}.csv", dtype=str)

        for index, row in input_csv_data.iterrows():
            endpoint = row["endpoint"]
            entity_ref = row["entity_ref"]

            print(f"Case Reference: {entity_ref}")
            entity_ids = get_entity_ids(csv, entity_ref, engine, sirius_app_session)
            line_structure = {}
            line = ""

            for entity_id in entity_ids:
                endpoint_final = get_endpoint_final(entity_id, endpoint, csv)
                response_as_json = get_response_json(sirius_app_session, endpoint_final)
                json_blocks_from_response = get_list_of_json_blocks_from_response(
                    csv, response_as_json
                )
                line_structure = get_line_structure_object_from_json_blocks(
                    json_blocks_from_response, row, line_structure, csv
                )

            line_structure = deduplicate_and_clean(line_structure, csv)
            line = convert_structure_to_line(line_structure)

            with open(f"responses/{csv}_output.csv", "a") as csv_outfile:
                csv_outfile.write(line)


if __name__ == "__main__":
    main()
