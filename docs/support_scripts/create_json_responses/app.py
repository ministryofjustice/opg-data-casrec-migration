import requests
import json
import pandas as pd
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../migration_steps/shared")
from helpers import *

env_path = current_path / "../../../migration_steps/.env"
load_dotenv(dotenv_path=env_path)
base_url = os.environ.get("SIRIUS_FRONT_URL")
password = os.environ.get("API_TEST_PASSWORD")
environment = os.environ.get("ENVIRONMENT")


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


def create_a_session():
    base_url = os.environ.get("SIRIUS_FRONT_URL")
    user = "case.manager@opgtest.com"
    password = os.environ.get("API_TEST_PASSWORD")
    sess, headers_dict, status_code = get_session(base_url, user, password)
    session = {
        "sess": sess,
        "headers_dict": headers_dict,
        "status_code": status_code,
        "base_url": base_url,
    }

    return session


def get_entity_ids(session, entity, search_field, search_value, csv_type):
    extra_headers = {"content-type": "application/json"}
    full_headers = {**session["headers_dict"], **extra_headers}

    data_raw = {
        "from": 0,
        "index": entity,
        "query": {
            "simple_query_string": {
                "query": search_value,
                "fields": ["searchable", search_field],
                "default_operator": "AND",
            }
        },
        "size": 5,
    }

    response = session["sess"].post(
        f'{session["base_url"]}/api/advanced-search',
        headers=full_headers,
        data=json.dumps(data_raw),
    )

    search_result = json.loads(response.text)

    ids = []

    if search_result["hits"]["total"] > 0:
        if csv_type in ["clients", "bonds"]:
            entity_id = search_result["hits"]["hits"][0]["_id"]

            print(entity_id)

            if csv_type == "bonds":
                bonds = get_bond_entity_ids(session, entity_id)
                for bond in bonds:
                    ids.append(bond)
            else:
                ids.append(entity_id)
        elif csv_type in ["orders", "supervision_level", "deputies"]:
            cases = search_result["hits"]["hits"][0]["_source"]["cases"]
            for case in cases:
                if case["caseType"] == "ORDER":
                    if csv_type == "deputies":
                        deputies = get_deputy_entity_ids(session, case["id"])
                        for deputy in deputies:
                            ids.append(deputy)
                    else:
                        ids.append(case["id"])
    return ids


def rationalise_var(v, json_obj):
    try:
        response_var = eval(v)
        if response_var is None:
            response_var = ""
        else:
            response_var = str(response_var)
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


def restructure_text(col):
    col_restructured = sorted(set(col.split("|")))
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


def get_bond_entity_ids(conn, entity_id):
    response = conn["sess"].get(
        f'{conn["base_url"]}/api/v1/clients/{entity_id}/orders',
        headers=conn["headers_dict"],
    )

    print(response.text)

    json_obj = json.loads(str(response.text))
    print(json_obj)

    cases = json_obj["cases"]

    bonds = []
    for case in cases:

        print(case["bond"])
        try:
            order_id = case["id"]
        except Exception:
            order_id = ""

        try:
            bond_id = case["bond"]["id"]
        except Exception:
            bond_id = ""

        if len(str(order_id)) > 0 and len(str(bond_id)) > 0:
            bond = {"order_id": order_id, "bond_id": bond_id}
            bonds.append(bond)

    return bonds


def get_deputy_entity_ids(conn, entity_id):
    response = conn["sess"].get(
        f'{conn["base_url"]}/api/v1/orders/{entity_id}', headers=conn["headers_dict"],
    )

    json_obj = json.loads(response.text)
    deputies = json_obj["deputies"]

    deputy_ids = []
    for deputy in deputies:
        try:
            deputy_id = deputy["deputy"]["id"]
        except Exception:
            deputy_id = ""

        if len(str(deputy_id)) > 0:
            deputy_ids.append(deputy_id)

    return deputy_ids


def get_endpoint_final(entity_id, endpoint, csv):
    if csv == "bonds":
        endpoint_final = (
            str(endpoint)
            .replace("{id}", str(entity_id["order_id"]))
            .replace("{id2}", str(entity_id["bond_id"]))
        )
    else:
        endpoint_final = str(endpoint).replace("{id}", str(entity_id))

    return endpoint_final


clients_headers = [
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
    '["phoneNumber"]',
    '["correspondenceByPost"]',
    '["correspondenceByPhone"]',
    '["correspondenceByEmail"]',
    '["personType"]',
    '["clientStatus"]["handle"]',
    '["clientStatus"]["label"]',
    '["clientAccommodation"]["handle"]',
    '["clientAccommodation"]["label"]',
    '["supervisionCaseOwner"]["name"]',
    '["supervisionCaseOwner"]["phoneNumber"]',
    '["maritalStatus"]',
]


deputies_headers = [
    '["email"]',
    '["addressLine1"]',
    '["postcode"]',
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
    '["bondProvider"]["name"]',
    '["requiredBondAmount"]',
    '["referenceNumber"]',
]

supervision_level_headers = [
    '["latestSupervisionLevel"]["appliesFrom"]',
    '["latestSupervisionLevel"]["supervisionLevel"]["handle"]',
    '["latestSupervisionLevel"]["assetLevel"]["handle"]',
]

csvs = ["bonds"]

search_headers = [
    "endpoint",
    "entity_ref",
    "search_entity",
    "search_field",
    "full_check",
]

for csv in csvs:
    head_line = ""
    for header in search_headers:
        head_line = head_line + header + ","
    for header in eval(f"{csv}_headers"):
        head_line = head_line + header + ","
    head_line = head_line[:-1]
    head_line = head_line + "\n"

    with open(f"responses/{csv}_output.csv", "w") as csv_outfile:
        csv_outfile.write(head_line)

    csv_data = pd.read_csv(f"{csv}.csv", dtype=str)
    columns = csv_data.columns.tolist()
    conn = create_a_session()

    #     response = conn["sess"].get('http://localhost:8080/api/v1/deputies/43', headers=conn["headers_dict"])
    #     print(response.text)

    # Iterate over rows
    for index, row in csv_data.iterrows():
        endpoint = row["endpoint"]
        entity_ref = row["entity_ref"]
        search_entity = row["search_entity"]
        search_field = row["search_field"]
        entity_ids = get_entity_ids(conn, search_entity, search_field, entity_ref, csv)

        line_struct = {}
        line = ""

        for entity_id in entity_ids:

            endpoint_final = get_endpoint_final(entity_id, endpoint, csv)
            print(endpoint_final)

            response = conn["sess"].get(
                f'{conn["base_url"]}{endpoint_final}', headers=conn["headers_dict"],
            )
            print(f'{conn["base_url"]}{endpoint_final}')
            print(response.text)
            print(response.status_code)

            json_obj = json.loads(response.text)

            with open(f"responses/{csv}_{entity_ref}.json", "w") as outfile:
                json.dump(json_obj, outfile, indent=4, sort_keys=False)

            for header in search_headers:
                curr_var = eval(f'row["{header}"]')
                try:
                    line_struct[header] = line_struct[header] + curr_var + "|"
                except Exception:
                    line_struct[header] = curr_var + "|"
            for header in eval(f"{csv}_headers"):
                var_to_eval = f"json_obj{header}"
                rationalised_var = rationalise_var(var_to_eval, json_obj)
                try:
                    line_struct[header] = line_struct[header] + rationalised_var + "|"
                except Exception:
                    line_struct[header] = rationalised_var + "|"

        for header in eval(f"{csv}_headers") + search_headers:
            try:
                line_struct_header = line_struct[header]
            except KeyError:
                line_struct_header = ""

            col_restruct_text = restructure_text(line_struct_header)
            line_struct[header] = col_restruct_text

        for attr, value in line_struct.items():
            line = line + value + ","

        line = line[:-1]
        line = line + "\n"
        with open(f"responses/{csv}_output.csv", "a") as csv_outfile:
            csv_outfile.write(line)
