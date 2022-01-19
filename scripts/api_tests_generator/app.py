import requests
import json
import pandas as pd
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from jsonpath_ng import parse

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../migration_steps/shared")
from helpers import get_config

env_path = current_path / "../../migration_steps/.env"
load_dotenv(dotenv_path=env_path)
print_extra_info = True
base_url = os.environ.get("SIRIUS_FRONT_URL")
password = os.environ.get("API_TEST_PASSWORD")
environment = os.environ.get("ENVIRONMENT")
config = get_config(environment)
db_conn_string = config.get_db_connection_string("target")
engine = create_engine(db_conn_string)
response_dir = "responses"

csvs = [
    "deputy_fee_payer",
    "clients",
    "orders",
    "bonds",
    "deputies",
    "deputy_orders",
    "deputy_clients",
    "supervision_level",
    "client_death_notifications",
    "deputy_death_notifications",
    "deputy_warnings",
    "client_warnings",
    "crec",
    "visits",
    "invoices",
    "tasks",
    "deputy_notes",
    "client_notes",
    "client_status",
]

search_headers = [
    "endpoint",
    "entity_ref",
    "json_locator",
    "test_purpose",
]


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
        "preqa": "opg+siriussmoketest@digital.justice.gov.uk",
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
        SELECT id as id
        FROM persons
        WHERE caserecnumber = '{caserecnumber}'
        AND clientsource = 'CASRECMIGRATION'"""

    order_id_sql = f"""
        SELECT c.id as id
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
        "client_warnings",
        "crec",
        "visits",
        "reports",
        "invoices",
        "tasks",
        "client_notes",
        "client_status",
    ]:
        entity_ids = engine.execute(person_id_sql)
        if entity_ids.rowcount > 1:
            print(f"Too many matching rows for {caserecnumber}")
        elif entity_ids.rowcount < 1:
            print(f"No matching rows for {caserecnumber}")
        else:
            for entity_id in entity_ids.mappings():
                ids.append(entity_id["id"])
    elif csv_type in [
        "orders",
        "bonds",
        "supervision_level",
        "deputies",
        "deputy_warnings",
        "deputy_clients",
        "deputy_orders",
        "deputy_death_notifications",
        "deputy_fee_payer",
        "deputy_notes",
    ]:
        entity_ids = engine.execute(order_id_sql)
        if entity_ids.rowcount < 1:
            print(f"No matching rows for {caserecnumber}")
        else:
            for entity_id_row in entity_ids.mappings():
                entity_id = entity_id_row["id"]

                if csv_type in [
                    "deputies",
                    "deputy_clients",
                    "deputy_warnings",
                    "deputy_death_notifications",
                    "deputy_notes",
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


def rationalise(v):
    response_var = "" if v is None else str(v)

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
        f'{conn["base_url"]}/api/v1/orders/{entity_id}',
        headers=conn["headers_dict"],
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
        f'{conn["base_url"]}/api/v1/orders/{entity_id}',
        headers=conn["headers_dict"],
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

    if print_extra_info:
        print(f"Endpoint: {endpoint_final}")
    return endpoint_final


def generate_csv_headers_line(search_headers, csv):
    header_line = ""
    for search_header in search_headers:
        header_line = header_line + search_header + ","
    header_line = header_line + "api_response\n"

    return header_line


def get_response_json(
    sirius_app_session,
    endpoint_final,
):
    response = sirius_app_session["sess"].get(
        f'{sirius_app_session["base_url"]}{endpoint_final}',
        headers=sirius_app_session["headers_dict"],
    )

    if print_extra_info:
        print(response.text)
        print(response.status_code)

    return json.loads(response.text)


def get_line_structure(response_as_json, row, line_structure, csv, json_locator):
    for search_header in search_headers:
        row_value_from_input_csv = eval(f'row["{search_header}"]')
        try:
            line_structure[search_header] = (
                line_structure[search_header] + row_value_from_input_csv + "|"
            )
        except Exception:
            # This handles adding the first occurrence
            line_structure[search_header] = row_value_from_input_csv + "|"

    json_path_expression = parse(json_locator)

    for match in json_path_expression.find(response_as_json):
        rationalised_match = rationalise(match.value)
        try:
            line_structure["api_result"] = (
                line_structure["api_result"] + rationalised_match + "|"
            )
        except Exception:
            # This handles adding the first occurrence
            line_structure["api_result"] = rationalised_match + "|"

    return line_structure


def deduplicate_and_clean(line_structure, csv):
    all_headers = [
        {"dedupe": False, "headers": ["api_result"]},
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
    if not os.path.exists(response_dir):
        os.makedirs(response_dir)

    sirius_app_session = create_a_session(base_url, password)

    for csv in csvs:
        print(f"STARTING - {csv}")
        full_header_line = generate_csv_headers_line(search_headers, csv)

        with open(f"{response_dir}/{csv}.csv", "w") as csv_out_file:
            csv_out_file.write(full_header_line)

        input_csv_data = pd.read_csv(f"input_files/{csv}.csv", dtype=str)

        for index, row in input_csv_data.iterrows():
            endpoint = row["endpoint"]
            entity_ref = row["entity_ref"]
            json_locator = row["json_locator"]
            test_purpose = row["test_purpose"]

            print(f"Case Reference: {entity_ref}, Purpose: {test_purpose}")
            entity_ids = get_entity_ids(csv, entity_ref, engine, sirius_app_session)
            # Line structure is an object that we use before converting to a a line string later
            line_structure = {}

            for entity_id in entity_ids:
                endpoint_final = get_endpoint_final(entity_id, endpoint, csv)
                response_as_json = get_response_json(sirius_app_session, endpoint_final)
                line_structure = get_line_structure(
                    response_as_json, row, line_structure, csv, json_locator
                )

            line_structure = deduplicate_and_clean(line_structure, csv)
            line = convert_structure_to_line(line_structure)

            with open(f"responses/{csv}.csv", "a") as csv_outfile:
                csv_outfile.write(line)


if __name__ == "__main__":
    main()
