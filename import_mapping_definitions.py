import json
from datetime import datetime
import logging
import shutil
import zipfile
import boto3
import os
import click
from botocore.exceptions import ClientError


def assume_aws_session(account, role):
    """
    Assume an AWS session so that we can access AWS resources as that account
    """

    client = boto3.client("sts")
    account_id = client.get_caller_identity()["Account"]
    print(f"Current users account: {account_id}")

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


def rename_folder(rename_from, rename_to):
    print(f"renaming {rename_from} to {rename_to}")
    try:
        os.rename(rename_from, rename_to)
    except FileNotFoundError:
        print(f"{rename_from} not found, aborting")


def make_directory(dir_name):
    print(f"creating directory {dir_name}")
    os.mkdir(dir_name)


def pull_zip_file(bucket, client, source, file_name, version):
    """
    Download latest version of file from s3 staged
    """

    version_details = {"version_id": None, "last_modified": None}

    try:
        if version is None:

            response = client.list_object_versions(
                Bucket=bucket, Prefix=f"{source}/{file_name}"
            )
            version_details["version_id"] = [
                x["VersionId"] for x in response["Versions"] if x["IsLatest"]
            ][0]
            last_modified = [
                x["LastModified"] for x in response["Versions"] if x["IsLatest"]
            ][0]
            version_details["last_modified"] = datetime.strftime(
                last_modified, "%Y-%m-%d %H:%M:%S"
            )

            client.download_file(bucket, f"{source}/{file_name}", file_name)

        else:
            head = client.head_object(Bucket=bucket, Key=f"{source}/{file_name}")
            version_details["version_id"] = version
            version_details["last_modified"] = datetime.strftime(
                head["LastModified"], "%Y-%m-%d %H:%M:%s"
            )
            client.download_file(
                bucket,
                f"{source}/{file_name}",
                file_name,
                ExtraArgs={"VersionId": version},
            )

    except ClientError as e:
        logging.error(e)

        return (False, version_details)
    print(
        f"Downloaded {file_name.split('/')[-1]} version {version_details['version_id']} last modified {version_details['last_modified']}"
    )

    return (True, version_details)


def extract_zip(file, extract_location):
    """
    Extract zip into previous mappings folder
    """

    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(extract_location)

    print(f"Extracted file to {extract_location}")


@click.command()
@click.option("--s3_source", default="merged")
@click.option("--version", default=None)
def main(s3_source, version):
    dirname = os.path.dirname(__file__)

    account = "288342028542"
    role = "operator"
    zip_file = "mappings.zip"
    folder_prefix = os.path.join(dirname, "migration_steps", "shared")
    bucket_name = "casrec-migration-mappings-development"
    try:
        if os.path.isdir(f"{folder_prefix}/mapping_definitions_old"):
            shutil.rmtree(f"{folder_prefix}/mapping_definitions")
            shutil.rmtree(f"{folder_prefix}/mapping_spreadsheet")
            rename_folder(
                f"{folder_prefix}/mapping_definitions_old",
                f"{folder_prefix}/mapping_definitions",
            )
    except FileNotFoundError:
        pass

    rename_folder(
        f"{folder_prefix}/mapping_definitions",
        f"{folder_prefix}/mapping_definitions_old",
    )
    s3_session = assume_aws_session(account, role)
    client = s3_session.client("s3")

    success, version_details = pull_zip_file(
        bucket_name, client, s3_source, zip_file, version
    )
    if success:
        extract_zip(zip_file, f"{folder_prefix}")
        os.remove(zip_file)

        with open(
            f"{folder_prefix}/mapping_definitions/summary/version.json", "w+"
        ) as version_file:
            version_file.write(json.dumps(version_details))
    else:
        print("Something failed while getting the zip file")


if __name__ == "__main__":
    main()
