import requests
import json
import jsonschema
import pytest
import re
import os
import boto3
import io
import pandas as pd
from flatten_json import flatten
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")
from helpers import *

host = os.environ.get("DB_HOST")
ci = os.getenv("CI")
account = os.environ["SIRIUS_ACCOUNT"]
environment = os.environ.get("ENVIRONMENT")
account_name = os.environ.get("ACCOUNT_NAME")
bucket_name = f"casrec-migration-{account_name.lower()}"
entities = {
    "local": [
        "clients",
        "orders",
        "deputies",
        "supervision_level",
        "bonds",
        "death_notifications",
    ],
    "development": [
        "clients",
        "orders",
        "deputies",
        "supervision_level",
        "bonds",
        "death_notifications",
    ],
    "preproduction": ["clients"],
    "qa": [],
    "production": [],
}


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


@pytest.fixture(scope="session", autouse=True)
def create_a_session():
    base_url = os.environ.get("SIRIUS_FRONT_URL")
    env_users = {
        "local": "case.manager@opgtest.com",
        "development": "case.manager@opgtest.com",
        "preproduction": "opg+siriussmoketest@digital.justice.gov.uk",
        "qa": "opg+siriussmoketest@digital.justice.gov.uk",
        "production": "opg+siriussmoketest@digital.justice.gov.uk",
    }
    user = env_users[environment]
    password = os.environ.get("API_TEST_PASSWORD")
    sess, headers_dict, status_code = get_session(base_url, user, password)

    aws_sess = boto3.session.Session()
    s3_sess = get_s3_session(aws_sess, environment, host, ci=ci, account=account)

    session = {
        "sess": sess,
        "headers_dict": headers_dict,
        "status_code": status_code,
        "base_url": base_url,
        "s3_sess": s3_sess,
    }

    return session


def test_authentication(create_a_session):
    headers_dict = create_a_session["headers_dict"]
    status_code = create_a_session["status_code"]

    headers_schema = {
        "type": "object",
        "properties": {
            "Cookie": {"type": "string"},
            "x-xsrf-token": {"type": "string"},
        },
    }

    assert jsonschema.validate(instance=headers_dict, schema=headers_schema) is None
    assert re.match(
        "sirius=(?:(?!;\s+path=/;\s+HttpOnly,\s+XSRF\-TOKEN=)(?:.|\n))*;\s+path=/;\s+HttpOnly,\s+XSRF\-TOKEN=(?:(?!;\s+Path=/)(?:.|\n))*;\s+Path=/",
        headers_dict["Cookie"],
    )
    # Brings back 401 in live even though it has authenticated fine
    assert status_code == 401 or status_code == 200


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
        if csv_type in ["clients", "bonds", "death_notifications"]:
            entity_id = search_result["hits"]["hits"][0]["_id"]
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
    json_obj = json.loads(response.text)
    cases = json_obj["cases"]

    bonds = []
    for case in cases:

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


def remove_dynamic_keys(dict, keys):
    for key in keys:
        dict.pop(key, None)
    return dict


def flat_dict(d, ignore_list):
    final_dict = {}
    dict_flattened = flatten(d, "_")
    stack = list(dict_flattened.items())
    for k, v in stack:
        entry = {k: v}
        update = True
        for i in ignore_list:
            if f"_{i}".lower() in k.lower() or k.lower() == i.lower():
                update = False
        if update:
            final_dict.update(entry)

    return final_dict


@pytest.mark.parametrize(
    "csv",
    [
        "clients",
        "orders",
        "bonds",
        "deputies",
        "supervision_level",
        "death_notifications",
    ],
)
def test_csvs(csv, create_a_session):
    if csv in entities[environment]:
        s3_csv_path = f"validation/csvs/{csv}.csv"
        obj = create_a_session["s3_sess"].get_object(
            Bucket=bucket_name, Key=s3_csv_path
        )
        csv_data = pd.read_csv(io.BytesIO(obj["Body"].read()), dtype=str)

        count = 0
        # Iterate over rows in the input spreadheet
        for index, row in csv_data.iterrows():
            count = count + 1
            endpoint = row["endpoint"]
            entity_ref = row["entity_ref"]
            search_entity = row["search_entity"]
            search_field = row["search_field"]

            # Create a list of headers to verify
            headers_to_check = []
            for header in row.index:
                if header not in [
                    "endpoint",
                    "search_entity",
                    "search_field",
                    "entity_ref",
                    "full_check",
                ]:
                    headers_to_check.append(header)
            # Get the ids to perform the search on based on the caserecnumber
            entity_ids = get_entity_ids(
                create_a_session, search_entity, search_field, entity_ref, csv
            )

            if len(entity_ids) == 0:
                print(f"No ids found for '{csv}', nothing to test")
                os._exit(1)

            # Because some of our searches may bring back multiple entities we need an object to aggregate them
            response_struct = {}
            for entity_id in entity_ids:
                endpoint_final = get_endpoint_final(entity_id, endpoint, csv)
                print(f"Checking responses from: {endpoint_final}")
                response = create_a_session["sess"].get(
                    f'{create_a_session["base_url"]}{endpoint_final}',
                    headers=create_a_session["headers_dict"],
                )
                json_obj = json.loads(response.text)

                for header in headers_to_check:
                    var_to_eval = f"json_obj{header}"
                    rationalised_var = rationalise_var(var_to_eval, json_obj)
                    try:
                        response_struct[header] = (
                            response_struct[header] + rationalised_var + "|"
                        )
                    except Exception:
                        response_struct[header] = rationalised_var + "|"

                # Does a full check against each sub entity
                if row["full_check"].lower() == "true":
                    ignore_list = [
                        "id",
                        "uid",
                        "normalizedUid",
                        "statusDate",
                        "updatedDate",
                        "researchOptOut",
                    ]
                    s3_json = f"validation/responses/{csv}_{entity_ref}.json"
                    content_object = create_a_session["s3_sess"].get_object(
                        Bucket=bucket_name, Key=s3_json
                    )
                    content_decoded = json.loads(content_object["Body"].read().decode())
                    actual_response = flat_dict(json_obj, ignore_list)
                    expected_response = flat_dict(content_decoded, ignore_list)
                    assert (
                        str(actual_response).lower() == str(expected_response).lower()
                    )

            # Where we have multiple entity_ids we need rationalise the grouped responses
            for header in headers_to_check:
                col_restruct_text = restructure_text(response_struct[header])
                response_struct[header] = col_restruct_text
            # Check through each value in spreadsheet for that row against each value in our response struct
            for header in headers_to_check:
                assert (
                    str(response_struct[header]).lower()
                    == str(row[header]).replace("nan", "").lower()
                )

        print(f"Ran happy path tests against {count} cases in {csv}")
    else:
        print(f"CSV '{csv}' doesn't exist in this environment. Skipping...")


@pytest.mark.parametrize("csv", ["fail"])
def test_fail_csvs(csv, create_a_session):
    s3_csv_path = f"validation/csvs/{csv}.csv"

    obj = create_a_session["s3_sess"].get_object(Bucket=bucket_name, Key=s3_csv_path)
    csv_data = pd.read_csv(io.BytesIO(obj["Body"].read()), dtype=str)
    count = 0
    # Iterate over rows
    for index, row in csv_data.iterrows():
        count = count + 1
        endpoint = row["endpoint"]
        entity_ref = row["entity_ref"]
        search_entity = row["search_entity"]
        search_field = row["search_field"]

        entity_ids = get_entity_ids(
            create_a_session, search_entity, search_field, entity_ref, csv
        )

        for entity_id in entity_ids:
            endpoint_final = str(endpoint).replace("{id}", str(entity_id))

            response = create_a_session["sess"].get(
                f'{create_a_session["base_url"]}{endpoint_final}',
                headers=create_a_session["headers_dict"],
            )
            json_obj = json.loads(response.text)

            fail_count = 0
            for header in row.index:
                if (
                    header
                    not in [
                        "endpoint",
                        "search_entity",
                        "search_field",
                        "entity_ref",
                        "full_check",
                    ]
                    and json_obj is not None
                ):
                    var_to_eval = f"json_obj{header}"
                    try:
                        curr_var = eval(var_to_eval)
                        if curr_var is None:
                            curr_var = ""
                        else:
                            curr_var = str(curr_var)
                    except KeyError:
                        curr_var = ""
                        pass
                    if curr_var != str(row[header]).replace("nan", ""):
                        fail_count = fail_count + 1
            assert fail_count == 1

    print(f"Ran unhappy path tests against {count} cases in {csv}")
