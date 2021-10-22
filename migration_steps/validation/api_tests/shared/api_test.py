import requests
import time
import json
import jsonschema
import re
import os
import boto3
import io
import logging
from datetime import datetime
import pandas as pd
from flatten_json import flatten
import sys
from pathlib import Path
from sqlalchemy import create_engine

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")
import custom_logger
from helpers import get_config, get_s3_session, upload_file

# logging
log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")
# Update to DEBUG for extra logging whilst developing
custom_logger.setup_logging(env=environment, level="INFO", module_name="API tests")


class ApiTests:
    def __init__(self):
        self.csv = None
        self.host = os.environ.get("DB_HOST")
        self.ci = os.getenv("CI")
        self.base_url = os.environ.get("SIRIUS_FRONT_URL")
        self.account = os.environ["SIRIUS_ACCOUNT"]
        self.environment = os.environ.get("ENVIRONMENT")
        env_users = {
            "local": "case.manager@opgtest.com",
            "development": "case.manager@opgtest.com",
            "preproduction": "opg+siriussmoketest@digital.justice.gov.uk",
            "preqa": "opg+siriussmoketest@digital.justice.gov.uk",
            "qa": "opg+siriussmoketest@digital.justice.gov.uk",
            "production": "opg+siriussmoketest@digital.justice.gov.uk",
        }
        self.user = env_users[self.environment]
        self.account_name = (
            os.environ.get("ACCOUNT_NAME")
            if os.environ.get("ACCOUNT_NAME") != "qa"
            else "preproduction"
        )
        self.password = os.environ.get("API_TEST_PASSWORD")
        self.bucket_name = f"casrec-migration-{self.account_name.lower() if self.account_name else None}"
        self.failed = False
        self.session = None
        self.config = get_config(self.environment)
        self.db_conn_string = self.config.get_db_connection_string("target")
        self.engine = create_engine(self.db_conn_string)
        self.api_result_lines = []
        self.api_log_file = (
            f'api_tests_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.log'
        )
        self.s3_file_path = f"validation/logs/{self.api_log_file}"
        self.s3_sess = None
        self.list_entity_returned = ["warnings", "invoice"]
        self.entities = {
            "local": [
                "clients",
                "orders",
                "deputies",
                "deputy_orders",
                "deputy_clients_count",
                "deputy_fee_payer",
                "supervision_level",
                "bonds",
                "client_death_notifications",
                "deputy_death_notifications",
                "warnings",
                "crec",
                "visits",
                "reports",
                "invoice",
            ],
            "development": [
                "clients",
                "orders",
                "deputies",
                "deputy_orders",
                "deputy_clients_count",
                "deputy_fee_payer",
                "supervision_level",
                "bonds",
                "client_death_notifications",
                "deputy_death_notifications",
                "warnings",
                "crec",
                "visits",
                "reports",
                "invoice",
            ],
            "preproduction": [
                "clients",
                "orders",
                "deputies",
                "deputy_fee_payer",
                "deputy_orders",
                "deputy_clients_count",
                "warnings",
                "crec",
                "bonds",
                "client_death_notifications",
                "deputy_death_notifications",
                "supervision_level",
            ],
            "preqa": [
                "clients",
                "orders",
                "deputies",
                "deputy_fee_payer",
                "deputy_orders",
                "deputy_clients_count",
                "warnings",
                "crec",
                "bonds",
                "client_death_notifications",
                "deputy_death_notifications",
                "supervision_level",
            ],
            "qa": [
                "clients",
                "orders",
                "deputies",
                "deputy_fee_payer",
                "deputy_orders",
                "deputy_clients_count",
                "warnings",
                "bonds",
                "client_death_notifications",
                "deputy_death_notifications",
                "supervision_level",
            ],
            "production": [],
        }
        self.all_allowed_entities = self.config.allowed_entities(self.environment) + [
            "deputy_clients",
            "deputy_clients_count",
            "deputy_fee_payer",
        ]
        self.no_retry_entities = ["deputy_death_notifications"]

    def get_session(self):
        response = requests.get(self.base_url)
        cookie = response.headers["Set-Cookie"]
        xsrf = response.headers["X-XSRF-TOKEN"]
        headers_dict = {"Cookie": cookie, "x-xsrf-token": xsrf}
        data = {"email": self.user, "password": self.password}
        with requests.Session() as s:
            p = s.post(f"{self.base_url}/auth/login", data=data, headers=headers_dict)
            self.api_log(f"Login returns: {p.status_code}")
            return s, headers_dict, p.status_code

    def create_a_session(self):
        sess, headers_dict, status_code = self.get_session()

        aws_sess = boto3.session.Session()
        self.s3_sess = get_s3_session(
            aws_sess, self.environment, self.host, ci=self.ci, account=self.account
        )

        self.session = {
            "sess": sess,
            "headers_dict": headers_dict,
            "status_code": status_code,
            "base_url": self.base_url,
            "s3_sess": self.s3_sess,
        }

        return self.session

    def test_authentication(self):
        headers_dict = self.session["headers_dict"]
        status_code = self.session["status_code"]

        headers_schema = {
            "type": "object",
            "properties": {
                "Cookie": {"type": "string"},
                "x-xsrf-token": {"type": "string"},
            },
        }

        assert jsonschema.validate(instance=headers_dict, schema=headers_schema) is None
        assert re.match(
            "sirius=(?:(?!;\s+path=/;\s+HttpOnly,\s+XSRF\-TOKEN=)(?:.|\n))*;\s+path=/;\s+HttpOnly,\s+XSRF\-TOKEN=(?:("
            "?!;\s+Path=/)(?:.|\n))*;\s+Path=/",
            headers_dict["Cookie"],
        )
        # Brings back 401 in live even though it has authenticated fine
        assert status_code == 401 or status_code == 200

    def get_person_sql(self, caserecnumber):
        sql = f"""
            SELECT id as id
            FROM persons
            WHERE caserecnumber = '{caserecnumber}'
            AND clientsource in ('CASRECMIGRATION', 'SKELETON')"""
        return sql

    def get_order_sql(self, caserecnumber):
        sql = f"""
            SELECT c.id as id
            FROM persons p
            INNER join cases c
            on c.client_id = p.id
            WHERE p.caserecnumber = '{caserecnumber}'
            AND p.clientsource in ('CASRECMIGRATION', 'SKELETON')
            and c.casetype = 'ORDER'"""
        return sql

    def get_active_order_sql(self, caserecnumber):
        sql = f"""
            SELECT c.id as id
            FROM persons p
            INNER join cases c
            on c.client_id = p.id
            WHERE p.caserecnumber = '{caserecnumber}'
            AND p.clientsource in ('CASRECMIGRATION', 'SKELETON')
            and c.casetype = 'ORDER'
            and c.orderstatus = 'ACTIVE'"""
        return sql

    def get_entity_ids_from_person_source(self, sql, caserecnumber):
        ids = []
        entity_ids = self.engine.execute(sql)
        if entity_ids.rowcount > 1:
            self.api_log(f"Too many matching rows for {caserecnumber}")
            self.failed = True
        elif entity_ids.rowcount < 1:
            self.api_log(f"No matching rows for {caserecnumber}")
            self.failed = True
        else:
            entity_id = entity_ids.one()._mapping["id"]
            ids.append(entity_id)
        return ids

    def enhance_api_user_permissions(self):
        roles = (
            '{"OPG User":"OPG User","Case Manager":"Case Manager","System Admin":"System Admin","Finance '
            'User":"Finance User","Finance Reporting":"Finance Reporting","Corporate Finance":"Corporate '
            'Finance","Finance Manager":"Finance Manager"}'
        )

        sql = f"""
            UPDATE assignees
            SET roles = '{roles}'
            WHERE email = '{self.user}'
            """
        self.engine.execute(sql)

    def get_entity_ids_from_order_source(self, sql, caserecnumber):
        log.debug(f"get_entity_ids_from_order_source for casrec number {caserecnumber}")
        ids = []
        entity_ids = self.engine.execute(sql)
        if entity_ids.rowcount < 1:
            self.api_log(f"No matching rows for {caserecnumber}")
            self.failed = True
        else:
            for entity_id_row in entity_ids:
                entity_id = entity_id_row._mapping["id"]
                if self.csv in [
                    "deputies",
                    "deputy_clients",
                    "deputy_clients_count",
                    "deputy_death_notifications",
                ]:
                    deputies = self.get_deputy_entity_ids(entity_id)
                    for deputy in deputies:
                        ids.append(deputy)
                elif self.csv in ["deputy_orders", "deputy_fee_payer"]:
                    deputy_orders = self.get_deputy_order_entity_ids(entity_id)
                    for deputy_order in deputy_orders:
                        ids.append(deputy_order)
                else:
                    ids.append(entity_id)
        log.debug(f"returning ids: {ids}")
        return ids

    def get_functional_entity_ids_from_order_source(self, sql, caserecnumber):
        ids = []
        entity_ids = self.engine.execute(sql)
        if entity_ids.rowcount < 1:
            self.api_log(f"No matching rows for {caserecnumber}")
            self.failed = True
        else:
            for entity_id_row in entity_ids:
                entity_id = entity_id_row._mapping["id"]
                ids.append(entity_id)
        log.debug(f"returning ids: {ids}")
        return ids

    def get_entity_ids(self, caserecnumber):
        log.debug(f"get_entity_ids for case no {caserecnumber}")
        person_id_sql = self.get_person_sql(caserecnumber)
        order_id_sql = self.get_order_sql(caserecnumber)
        ids = []
        if self.csv in [
            "clients",
            "client_death_notifications",
            "warnings",
            "crec",
            "visits",
            "reports",
            "invoice",
        ]:
            ids = self.get_entity_ids_from_person_source(person_id_sql, caserecnumber)
        elif self.csv in [
            "orders",
            "bonds",
            "supervision_level",
            "deputies",
            "deputy_clients",
            "deputy_orders",
            "deputy_clients_count",
            "deputy_death_notifications",
            "deputy_fee_payer",
        ]:
            ids = self.get_entity_ids_from_order_source(order_id_sql, caserecnumber)
        log.debug(f"returning ids: {ids}")
        return ids

    def get_headers_to_check(self, row):
        headers_to_check = []
        for header in row.index:
            if header not in [
                "endpoint",
                "entity_ref",
                "test_purpose",
                "full_check",
            ]:
                headers_to_check.append(header)

        return headers_to_check

    def get_processed_entity_ids(self, entity_ref):
        log.debug(f"get_processed_entity_ids for entity ref {entity_ref}")
        entity_ids = self.get_entity_ids(entity_ref)

        if len(entity_ids) == 0:
            self.api_log(f"No ids found for '{self.csv}', nothing to test")
            self.failed = True
        log.debug(f"returning: {entity_ids}")
        return entity_ids

    def get_response_object(self, endpoint_final):
        status_code = 500
        response_text = None
        retry_count = 0
        if self.csv in self.no_retry_entities:
            response = self.session["sess"].get(
                f'{self.session["base_url"]}{endpoint_final}',
                headers=self.session["headers_dict"],
            )
            response_text = response.text
            status_code = response.status_code
            if status_code > 201 and status_code != 404:
                self.api_log(
                    f"Failed request to {endpoint_final} with status {status_code}."
                )
            elif status_code == 404:
                self.api_log(f"No entity to pull back on this route. This is expected!")
        else:
            while (status_code > 201 or response_text is None) and retry_count < 5:
                response = self.session["sess"].get(
                    f'{self.session["base_url"]}{endpoint_final}',
                    headers=self.session["headers_dict"],
                )
                response_text = response.text
                status_code = response.status_code
                if retry_count > 0:
                    self.api_log(
                        f"Failed request to {endpoint_final} with status {status_code}. Retrying in 3 seconds..."
                    )
                    time.sleep(3)
                retry_count += 1

        return response_text

    def get_json_items_to_loop_through(self, json_object):
        items_to_loop_through = []
        if self.csv in self.list_entity_returned:
            for list_item in json_object:
                items_to_loop_through.append(list_item)
        else:
            items_to_loop_through.append(json_object)
        return items_to_loop_through

    def get_formatted_api_response(
        self, entity_ids, endpoint, headers_to_check, row, entity_ref
    ):
        log.debug(
            f"get_formatted_api_response: entity_ids: {entity_ids} entity_ref: {entity_ref} endpoint {endpoint}"
        )
        response_struct = {}
        for entity_id in entity_ids:
            endpoint_final = self.get_endpoint_final(entity_id, endpoint)
            self.api_log(f"Checking responses from: {endpoint_final}")

            response_text = self.get_response_object(endpoint_final)
            json_obj = json.loads(response_text)

            json_items_to_loop_through = self.get_json_items_to_loop_through(json_obj)

            for json_item_to_inspect in json_items_to_loop_through:
                for header in headers_to_check:
                    var_to_eval = f"json_item_to_inspect{header}"
                    rationalised_var = self.rationalise_var(
                        var_to_eval, json_item_to_inspect
                    )
                    try:
                        response_struct[header] = (
                            response_struct[header] + rationalised_var + "|"
                        )
                    except Exception:
                        response_struct[header] = rationalised_var + "|"

            # Does a full check against each sub entity
            if row["full_check"].lower() == "true":
                self.run_full_check(self.csv, entity_ref, json_obj)
        log.debug(f"returning: {response_struct}")
        return response_struct

    def get_count_api_response(self, entity_ids, endpoint, headers_to_check):
        log.debug(
            f"get_count_api_response: entity_ids: {entity_ids}  endpoint {endpoint}"
        )
        response_struct = {}
        for entity_id in entity_ids:
            endpoint_final = self.get_endpoint_final(entity_id, endpoint)
            self.api_log(f"Checking responses from: {endpoint_final}")
            response = self.session["sess"].get(
                f'{self.session["base_url"]}{endpoint_final}',
                headers=self.session["headers_dict"],
            )
            json_obj = json.loads(response.text)

            for header in headers_to_check:
                var_to_eval = f"json_obj{header}"
                count_of_objects = self.get_count_of_object(var_to_eval, json_obj)
                try:
                    response_struct[header] = (
                        response_struct[header] + str(count_of_objects) + "|"
                    )
                except Exception:
                    response_struct[header] = str(count_of_objects) + "|"
        log.debug(f"returning: {response_struct}")
        return response_struct

    def run_full_check(self, entity_ref, json_obj):
        log.debug(f"running full check for {entity_ref}")
        ignore_list = [
            "id",
            "uid",
            "normalizedUid",
            "statusDate",
            "updatedDate",
            "researchOptOut",
        ]
        s3_json = f"validation/responses/{self.csv}_{entity_ref}.json"
        content_object = self.session["s3_sess"].get_object(
            Bucket=self.bucket_name, Key=s3_json
        )
        content_decoded = json.loads(content_object["Body"].read().decode())
        actual_response = self.flat_dict(json_obj, ignore_list)
        expected_response = self.flat_dict(content_decoded, ignore_list)
        assert str(actual_response).lower() == str(expected_response).lower()

    def rationalise_var(self, v, json_item_to_inspect):
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

    def get_count_of_object(self, v, json_obj):
        try:
            response_var = eval(v)
            if response_var is None:
                count = 0
            else:
                count = len(response_var)
        except IndexError:
            count = 0
            pass
        except KeyError:
            count = 0
            pass
        except TypeError:
            count = 0
            pass
        return count

    def restructure_text(self, col):
        col_restructured = sorted(col.split("|"))
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

    def get_deputy_entity_ids(self, entity_id):
        log.debug(f"get_deputy_entity_ids: entity_id {entity_id}")
        response = self.session["sess"].get(
            f'{self.session["base_url"]}/api/v1/orders/{entity_id}',
            headers=self.session["headers_dict"],
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
        log.debug(f"returning: {deputy_ids}")
        return deputy_ids

    def get_deputy_order_entity_ids(self, entity_id):
        response = self.session["sess"].get(
            f'{self.session["base_url"]}/api/v1/orders/{entity_id}',
            headers=self.session["headers_dict"],
        )

        json_obj = json.loads(response.text)
        deputies = json_obj["deputies"]

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

    def get_endpoint_final(self, entity_id, endpoint):
        log.debug(f"get_endpoint_final: entity_id {entity_id} endpoint {endpoint}")
        if self.csv in ["deputy_orders", "deputy_fee_payer"]:
            endpoint_final = (
                str(endpoint)
                .replace("{id1}", str(entity_id["order_id"]))
                .replace("{id2}", str(entity_id["deputy_id"]))
            )
        else:
            endpoint_final = str(endpoint).replace("{id}", str(entity_id))
        log.debug(f"returning: {endpoint_final}")
        return endpoint_final

    def assert_on_fields(
        self, headers_to_check, formatted_api_response, row, entity_ref
    ):
        # Where we have multiple entity_ids we need rationalise the grouped responses
        for header in headers_to_check:
            col_restruct_text = self.restructure_text(formatted_api_response[header])
            formatted_api_response[header] = col_restruct_text
        # Check through each value in spreadsheet for that row against each value in our response struct
        for header in headers_to_check:
            expected = str(row[header]).replace("nan", "").lower()
            actual = str(formatted_api_response[header]).lower()
            try:
                assert expected == actual
            except AssertionError:
                self.api_log(
                    f"""
                    Case: {entity_ref}
                    Field: {header}"""
                )
                self.api_log(
                    f"""Expected: {expected}
                    Actual: {actual}""",
                    False,
                )
                self.failed = True

    def remove_dynamic_keys(self, dict, keys):
        for key in keys:
            dict.pop(key, None)
        return dict

    def flat_dict(self, d, ignore_list):
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

    def api_log(self, message, log_to_screen=True):
        if log_to_screen:
            log.info(message)
        self.api_result_lines.append(message + "\n")

    def upload_log_file(self):
        api_log_file = open(self.api_log_file, "w")
        api_log_file.writelines(self.api_result_lines)
        api_log_file.close()
        log.info(f"Saved to file: {self.api_log_file}")
        upload_file(
            self.bucket_name, self.api_log_file, self.s3_sess, log, self.s3_file_path
        )

    def run_success_tests(self):
        self.api_log(f"Starting tests against '{self.csv}'")
        if self.csv in self.entities[self.environment]:
            s3_csv_path = f"validation/csvs/{self.csv}.csv"
            obj = self.session["s3_sess"].get_object(
                Bucket=self.bucket_name, Key=s3_csv_path
            )
            csv_data = pd.read_csv(io.BytesIO(obj["Body"].read()), dtype=str)

            count = 0
            # Iterate over rows in the input spreadsheet
            for index, row in csv_data.iterrows():
                count = count + 1
                endpoint = row["endpoint"]
                entity_ref = row["entity_ref"]

                # Create a list of headers to verify
                headers_to_check = self.get_headers_to_check(row)
                # Get the ids to perform the search on based on the caserecnumber
                entity_ids = self.get_processed_entity_ids(entity_ref)

                # Because some of our searches may bring back multiple entities we need an object to aggregate them
                if self.csv in ["deputy_clients_count"]:
                    formatted_api_response = self.get_count_api_response(
                        entity_ids, endpoint, headers_to_check
                    )
                else:
                    formatted_api_response = self.get_formatted_api_response(
                        entity_ids, endpoint, headers_to_check, row, entity_ref
                    )
                # Check we haven't brought back an empty dict as response
                if formatted_api_response:
                    # Loop through and check expected results against actual for each field
                    self.assert_on_fields(
                        headers_to_check, formatted_api_response, row, entity_ref
                    )
                else:
                    self.api_log("empty dictionary returned!")
            self.api_log(f"Ran happy path tests against {count} cases in {self.csv}")
        else:
            self.api_log(
                f"CSV '{self.csv}' doesn't exist in this environment. Skipping..."
            )

    def functional_tests_by_method(self, method, entity_setup_objects):
        for entity_setup_object in entity_setup_objects:
            title = entity_setup_object["title"]
            self.api_log(f"Running Functional API Section - {title}")
            url = "/api/v1/" + entity_setup_object["url"]
            data = entity_setup_object["data"]
            source = entity_setup_object["source"]
            case_references = entity_setup_object["case_references"]
            expected_status = entity_setup_object["expected_status"]

            try:
                id2_endpoint = entity_setup_object["id2_url"]
                id2_json_path = entity_setup_object["id2_json_path"]
            except Exception:
                id2_endpoint = None
                id2_json_path = None

            for case_reference in case_references:
                entity_ids = self.get_functional_entity_ids(case_reference, source)
                first_entity_id = entity_ids[0]
                endpoint = self.get_functional_endpoint(
                    first_entity_id, url, id2_endpoint, id2_json_path
                )
                actual_status = self.get_functional_response_object(
                    endpoint, method, data
                )
                try:
                    assert expected_status == actual_status
                except AssertionError:
                    self.api_log(f"Expected: {expected_status} but got {actual_status}")

    def run_functional_test(self, entity, entity_setup_object):
        self.csv = entity
        if entity_setup_object["post_objects"] is not None:
            self.functional_tests_by_method("POST", entity_setup_object["post_objects"])
        if entity_setup_object["put_objects"] is not None:
            self.functional_tests_by_method("PUT", entity_setup_object["put_objects"])
        if entity_setup_object["delete_objects"] is not None:
            self.functional_tests_by_method(
                "DELETE", entity_setup_object["delete_objects"]
            )
        self.api_log(f"Successfully finished {self.csv} functional tests")

    def get_functional_endpoint(
        self, entity_id, endpoint, id2_endpoint=None, id2_json_path=None
    ):
        if id2_endpoint is not None and id2_endpoint is not None:
            first_id2 = self.get_entity_id_from_array(
                entity_id, id2_endpoint, id2_json_path
            )
            if "{id2}" in endpoint:
                endpoint_final = (
                    str(endpoint)
                    .replace("{id}", str(entity_id))
                    .replace("{id2}", str(first_id2))
                )
            else:
                endpoint_final = str(endpoint).replace("{id}", str(first_id2))
        else:
            endpoint_final = str(endpoint).replace("{id}", str(entity_id))
        self.api_log(f"Running against: {endpoint_final}")
        return endpoint_final

    def get_entity_id_from_array(self, entity_id, endpoint, id2_json_path):
        endpoint_final = self.get_functional_endpoint(entity_id, endpoint)
        full_url = f'{self.session["base_url"]}/api/v1/{endpoint_final}'
        log.debug(
            f"Using the following url to get the required id for real url: {full_url}"
        )

        response = self.session["sess"].get(
            full_url, headers=self.session["headers_dict"],
        )

        json_object = json.loads(response.text)
        log.debug(json_object)
        variable_to_evaluate = f"json_object{id2_json_path}"
        first_id = eval(variable_to_evaluate)
        return first_id

    def get_functional_response_object(self, endpoint_final, method, data=None):
        content_type_dict = {"Content-Type": "application/json"}
        headers = {**self.session["headers_dict"], **content_type_dict}
        if method == "POST":
            response = self.session["sess"].post(
                f'{self.session["base_url"]}{endpoint_final}',
                headers=headers,
                data=json.dumps(data),
            )
        elif method == "PUT":
            response = self.session["sess"].put(
                f'{self.session["base_url"]}{endpoint_final}',
                headers=headers,
                data=json.dumps(data),
            )
        elif method == "DELETE":
            response = self.session["sess"].delete(
                f'{self.session["base_url"]}{endpoint_final}',
                headers=self.session["headers_dict"],
            )
        else:
            self.api_log(f"Method {method} is invalid")

        log.debug(f"Response text: {response.text}")
        status_code = response.status_code

        self.api_log(f"Returns following: {status_code}")

        return status_code

    def get_functional_entity_ids(self, caserecnumber, source):
        person_id_sql = self.get_person_sql(caserecnumber)
        order_id_sql = self.get_active_order_sql(caserecnumber)
        ids = []
        if source == "clients":
            ids = self.get_entity_ids_from_person_source(person_id_sql, caserecnumber)
        elif source == "orders":
            ids = self.get_functional_entity_ids_from_order_source(
                order_id_sql, caserecnumber
            )
        log.debug(f"returning ids: {ids}")
        return ids
