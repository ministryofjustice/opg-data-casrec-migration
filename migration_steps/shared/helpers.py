import json
import os
import boto3
from typing import Dict
from typing import List

from config import BaseConfig
from config import LocalConfig

from decorators import track_file_use
import logging

log = logging.getLogger("root")


def log_title(message: str) -> str:
    total_length = 100
    padded_word = f" {message} "
    left_filler_length = round((total_length - len(padded_word)) / 2)
    right_filler_length = total_length - len(padded_word) - left_filler_length

    left_filler = "=" * left_filler_length
    right_filler = "=" * right_filler_length

    log_string = left_filler + padded_word.upper() + right_filler

    return log_string


def get_current_directory():
    dirname = os.path.dirname(__file__)
    return dirname


def check_entity_enabled(entity_name, extra_entities=None):
    config = get_config(env=os.environ.get("ENVIRONMENT"))

    allowed_entities = config.allowed_entities(env=os.environ.get("ENVIRONMENT"))

    if extra_entities:
        required_entities = extra_entities + [entity_name]
    else:
        required_entities = [entity_name]

    if all(x in allowed_entities for x in required_entities):
        log.info(f"Entity '{entity_name}' is enabled")
        return True
    else:
        if entity_name not in allowed_entities:
            log.info(f"Entity '{entity_name}' is disabled")
        else:
            if extra_entities:
                disabled_entities = [
                    f"'{x}'" for x in required_entities if x not in allowed_entities
                ]
                log.info(
                    f"Entity '{entity_name}' relies on disabled entities {', '.join(disabled_entities)}, moving on"
                )
            else:
                log.info(f"Entity '{entity_name}' is disabled")
        return False


def list_all_mapping_files():
    dirname = get_current_directory()
    file_path = os.path.join(dirname, f"mapping_definitions")

    files = []
    for mapping_file in os.listdir(file_path):
        mapping_file_path = os.path.join(file_path, mapping_file)
        if os.path.isfile(mapping_file_path):
            files.append(mapping_file)
    return files


@track_file_use
def get_mapping_dict(
    file_name: str,
    stage_name: str = "",
    only_complete_fields: bool = False,
    include_pk: bool = True,
    include_fks: bool = True,
) -> Dict:
    dirname = get_current_directory()
    file_path = os.path.join(dirname, f"mapping_definitions/{file_name}.json")

    with open(file_path) as mapping_json:
        mapping_dict = json.load(mapping_json)

    if only_complete_fields:
        mapping_dict = {
            k: v
            for k, v in mapping_dict.items()
            if v["mapping_status"]["is_complete"] is True
        }
    if not include_pk:
        mapping_dict = {
            k: v
            for k, v in mapping_dict.items()
            if v["sirius_details"]["is_pk"] is not True
        }

    if not include_fks:
        mapping_dict = {
            k: v
            for k, v in mapping_dict.items()
            if v["sirius_details"]["fk_parents"] == ""
        }

    if stage_name:
        try:
            mapping_dict = {k: v[stage_name] for k, v in mapping_dict.items()}
        except KeyError:
            mapping_dict = {}

    return mapping_dict


def get_lookup_dict(file_name: str, include_sirius_details: bool = False) -> Dict:

    dirname = get_current_directory()
    file_path = os.path.join(
        dirname, f"mapping_definitions/lookups" f"/{file_name}.json"
    )

    with open(file_path) as lookup_json:
        lookup_dict = json.load(lookup_json)

        if len(lookup_dict) == 0:
            log.error(f"No data for lookup file {file_name}")

        if include_sirius_details:
            return lookup_dict
        else:
            return {k: v["sirius_mapping"] for k, v in lookup_dict.items()}


def get_additional_data_dict(file_name: str) -> Dict:

    dirname = get_current_directory()
    file_path = os.path.join(
        dirname, f"mapping_definitions/additional_data" f"/{file_name}.json"
    )

    with open(file_path) as additional_data_json:
        additional_data_dict = json.load(additional_data_json)

    return additional_data_dict


def get_all_additional_data_files():
    dirname = get_current_directory()
    file_path = os.path.join(dirname, f"mapping_definitions/additional_data")

    all_files = []
    for file in os.listdir(file_path):
        all_files.append(file)

    return all_files


def get_table_def(mapping_name: str = None) -> Dict:
    dirname = get_current_directory()
    file_path = os.path.join(
        dirname, f"mapping_definitions/tables/table_definitions.json"
    )

    with open(file_path) as table_data:
        table_data_dict = json.load(table_data)

    log.debug(json.dumps(table_data_dict[mapping_name], indent=4))
    return table_data_dict[mapping_name]


def get_all_lookup_dicts() -> Dict[str, List[str]]:
    dirname = get_current_directory()
    file_path = os.path.join(dirname, f"mapping_definitions/lookups")

    all_lookup_dicts = {}

    for json_file in os.listdir(file_path):
        json_file_path = os.path.join(file_path, json_file)
        if os.path.isfile(json_file_path):
            with open(json_file_path, "r") as lookup_json:
                lookup_dict = json.load(lookup_json)
                lookup_name = json_file.replace(".json", "")
                all_lookup_dicts[lookup_name] = lookup_dict

    return all_lookup_dicts


def get_all_mapped_fields(
    complete: bool = True, include_keys: bool = False
) -> Dict[str, List[str]]:
    dirname = get_current_directory()
    file_path = os.path.join(dirname, f"mapping_definitions")

    all_mapping_dicts = {}

    for json_file in os.listdir(file_path):
        json_file_path = os.path.join(file_path, json_file)
        if os.path.isfile(json_file_path):
            if "table_definition" in json_file_path:
                pass
            else:
                with open(json_file_path, "r") as definition_json:
                    def_dict = json.load(definition_json)

                    key_name = json_file.replace("_mapping.json", "")
                    if include_keys:
                        all_mapping_dicts[key_name] = [
                            k
                            for k, v in def_dict.items()
                            if v["mapping_status"]["is_complete"] is complete
                        ]
                    else:
                        all_mapping_dicts[key_name] = [
                            k
                            for k, v in def_dict.items()
                            if v["mapping_status"]["is_complete"] is complete
                            and v["sirius_details"]["is_pk"] is not True
                            and len(v["sirius_details"]["fk_parents"]) == 0
                        ]

    return all_mapping_dicts


def get_json_version():
    dirname = get_current_directory()
    file_path = os.path.join(dirname, f"mapping_definitions/summary/version.json")
    try:
        with open(file_path, "r") as version_file:
            return json.load(version_file)
    except Exception:
        return {"version_id": "", "last_modified": ""}


def get_config(env="local"):

    # envcheck - just setting log levels for local dev
    if env == "local":
        config = LocalConfig()
    else:
        config = BaseConfig()
    return config


def get_s3_session(session, environment, host, ci="false", account=None):
    # todo refactor and combine multiple instances of get_s3_session
    s3_session = session
    if environment == "local":
        if host == "localhost":
            stack_host = "localhost"
        else:
            stack_host = "localstack"
        s3 = s3_session.client(
            "s3",
            endpoint_url=f"http://{stack_host}:4572",
            aws_access_key_id="fake",
            aws_secret_access_key="fake",  # pragma: allowlist secret
        )
    elif ci == "true":
        s3_session = sirius_session(account)
        s3 = s3_session.client("s3")
    else:
        s3 = s3_session.client("s3")

    return s3


def upload_file(bucket, file_name, s3, log, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file, needs this encryption to work!
    s3.put_object(
        Body=open(file_name, "rb"),
        Bucket=bucket,
        Key=object_name,
        ServerSideEncryption="AES256",
        StorageClass="STANDARD",
    )

    log.debug(f"Uploaded {file_name.split('/')[-1]}")


def sirius_session(account):
    client = boto3.client("sts")
    role_to_assume = f"arn:aws:iam::{account}:role/migrations-ci"
    response = client.assume_role(
        RoleArn=role_to_assume, RoleSessionName="assumed_role"
    )

    session = boto3.Session(
        aws_access_key_id=response["Credentials"]["AccessKeyId"],
        aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
        aws_session_token=response["Credentials"]["SessionToken"],
    )

    return session


def get_list_of_s3_files(bucket_name, s3, paths):
    resp = s3.list_objects_v2(Bucket=bucket_name)
    files_in_bucket = []

    for obj in resp["Contents"]:
        file_folder = obj["Key"]
        fo = file_folder.split("/")[:-1]
        folder = "/".join(fo)
        fi = file_folder.split("/")[-1:]
        file = "/".join(fi)

        for path in paths:
            print(f"{file}, {folder}, {path}")
            if str(folder) == str(path):
                files_in_bucket.append(file)

    return files_in_bucket


def format_error_message(e):
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    err = template.format(type(e).__name__, e.args)

    return err


def assume_aws_session(account, role):
    """
    Assume an AWS session so that we can access AWS resources as that account
    """

    client = boto3.client("sts")

    role_to_assume = f"arn:aws:iam::{account}:role/{role}"
    response = client.assume_role(
        RoleArn=role_to_assume, RoleSessionName="assumed_role"
    )

    session = boto3.Session(
        aws_access_key_id=response["Credentials"]["AccessKeyId"],
        aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
        aws_session_token=response["Credentials"]["SessionToken"],
    )

    return session
