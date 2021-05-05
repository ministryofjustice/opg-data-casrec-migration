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


def get_entity_id(session, entity, search_field, search_value, csv_type):
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
        if csv_type in ["clients", "deputies"]:
            entity_id = search_result["hits"]["hits"][0]["_id"]
            ids.append(entity_id)
        elif csv_type == "orders":
            cases = search_result["hits"]["hits"][0]["_source"]["cases"]
            for case in cases:
                if case["caseType"] == "ORDER":
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

csvs = ["orders", "clients", "deputies"]

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

    print(head_line)

    with open(f"responses/{csv}_output.csv", "w") as csv_outfile:
        csv_outfile.write(head_line)

    csv_data = pd.read_csv(f"{csv}.csv", dtype=str)
    columns = csv_data.columns.tolist()
    conn = create_a_session()

    # Iterate over rows
    for index, row in csv_data.iterrows():
        endpoint = row["endpoint"]
        entity_ref = row["entity_ref"]
        search_entity = row["search_entity"]
        search_field = row["search_field"]
        entity_ids = get_entity_id(conn, search_entity, search_field, entity_ref, csv)

        line_struct = {}
        line = ""
        for entity_id in entity_ids:
            endpoint_final = str(endpoint).replace("{id}", str(entity_id))
            print(endpoint_final)
            response = conn["sess"].get(
                f'{conn["base_url"]}{endpoint_final}',
                headers=conn["headers_dict"],
            )
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
            col_restruct_text = restructure_text(line_struct[header])
            line_struct[header] = col_restruct_text

        for attr, value in line_struct.items():
            line = line + value + ","

        line = line[:-1]
        line = line + "\n"
        with open(f"responses/{csv}_output.csv", "a") as csv_outfile:
            csv_outfile.write(line)
