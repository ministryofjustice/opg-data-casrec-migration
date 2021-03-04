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
bucket_name = f"casrec-migration-{environment.lower()}"


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
    user = "case.manager@opgtest.com"
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


def get_entity_id(session, entity, search_field, search_value):
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

    entity_id = None
    if search_result["hits"]["total"] > 0:
        entity_id = search_result["hits"]["hits"][0]["_id"]

    return entity_id


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


@pytest.mark.parametrize("csv", ["clients"])
def test_csvs(csv, create_a_session):
    s3_csv_path = f"validation/csvs/{csv}.csv"

    obj = create_a_session["s3_sess"].get_object(Bucket=bucket_name, Key=s3_csv_path)
    csv_data = pd.read_csv(io.BytesIO(obj["Body"].read()))

    # Iterate over rows
    for index, row in csv_data.iterrows():
        endpoint = row["endpoint"]
        entity_ref = row["entity_ref"]
        search_entity = row["search_entity"]
        search_field = row["search_field"]
        entity_id = get_entity_id(
            create_a_session, search_entity, search_field, entity_ref
        )
        endpoint_final = str(endpoint).replace("{id}", str(entity_id))

        response = create_a_session["sess"].get(
            f'{create_a_session["base_url"]}{endpoint_final}',
            headers=create_a_session["headers_dict"],
        )
        json_obj = json.loads(response.text)

        for header in row.index:
            if header not in [
                "endpoint",
                "search_entity",
                "search_field",
                "entity_ref",
                "full_check",
            ]:
                var_to_eval = f"json_obj{header}"
                try:
                    curr_var = eval(var_to_eval)
                except KeyError:
                    curr_var = ""
                    pass
                assert curr_var == str(row[header]).replace("nan", "")
        if row["full_check"]:
            with open(f"responses/{csv}_{entity_ref}.json") as json_file:
                actual_response = flat_dict(json_obj, ["id", "uid"])
                expected_response = flat_dict(json.load(json_file), ["id", "uid"])

                assert actual_response == expected_response


@pytest.mark.parametrize("csv", ["fail"])
def test_fail_csvs(csv, create_a_session):
    s3_csv_path = f"validation/csvs/{csv}.csv"

    obj = create_a_session["s3_sess"].get_object(Bucket=bucket_name, Key=s3_csv_path)
    csv_data = pd.read_csv(io.BytesIO(obj["Body"].read()))

    # Iterate over rows
    for index, row in csv_data.iterrows():
        endpoint = row["endpoint"]
        entity_ref = row["entity_ref"]
        search_entity = row["search_entity"]
        search_field = row["search_field"]
        entity_id = get_entity_id(
            create_a_session, search_entity, search_field, entity_ref
        )
        endpoint_final = str(endpoint).replace("{id}", str(entity_id))

        response = create_a_session["sess"].get(
            f'{create_a_session["base_url"]}{endpoint_final}',
            headers=create_a_session["headers_dict"],
        )
        json_obj = json.loads(response.text)

        fail_count = 0
        for header in row.index:
            if header not in [
                "endpoint",
                "search_entity",
                "search_field",
                "entity_ref",
                "full_check",
            ]:
                var_to_eval = f"json_obj{header}"
                try:
                    curr_var = eval(var_to_eval)
                except KeyError:
                    curr_var = ""
                    pass
                if curr_var != str(row[header]).replace("nan", ""):
                    fail_count = fail_count + 1
        assert fail_count == 1

        if row["full_check"]:
            with open(f"responses/{csv}_{entity_ref}.json") as json_file:
                actual_response = flat_dict(json_obj, ["id", "uid"])
                expected_response = flat_dict(json.load(json_file), ["id", "uid"])

                assert actual_response != expected_response
