import difflib
import logging
import os
import sys
import zipfile
import click as click
import boto3
from botocore.exceptions import ClientError
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../migration_steps/shared")
from helpers import assume_aws_session

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
shared_path = f"{current_path}/../../migration_steps/shared"
mappings_path = f"{current_path}/../../mappings"

account = "288342028542"
previous_folder = "mapping_definitions_previous"
bucket_name = "casrec-migration-mappings-development"
output_file = "./mapping_definitions/summary/file_diffs.txt"
zip_file_prefix = "mappings"
ext = ".zip"
s3_folder = "merged"


def zip_dir(dirs_to_zip, zip_file):
    """
    Zip up directories locally
    """
    zip_path = Path(zip_file)
    if zip_path.exists():
        os.remove(zip_file)
        print("Zip file removed")
    zipf = zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED)
    for dir_to_zip in dirs_to_zip:
        full_dir = f"{dir_to_zip}"
        for root, dirs, files in os.walk(full_dir):
            for file in files:
                zipf.write(os.path.join(root, file))
    zipf.close()


def upload_file(bucket, file_name, client, object_name=None):
    """
    Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    try:
        transfer = boto3.s3.transfer.S3Transfer(client=client)
        transfer.upload_file(
            file_name,
            bucket,
            object_name,
            extra_args={"ServerSideEncryption": "AES256"},
        )
    except ClientError as e:
        logging.error(e)
        return False
    print(f"Uploaded {file_name.split('/')[-1]}")

    return True


def pull_latest_merged(bucket, client, file_name):
    """
    Download latest version of file from s3 staged
    """

    latest_merged = f"merged/{file_name}"
    try:
        client.download_file(bucket, latest_merged, file_name)
    except ClientError as e:
        logging.error(e)
        return False
    print(f"Downloaded {file_name.split('/')[-1]}")

    return True


def extract_zip(file, extract_location):
    """
    Extract zip into previous mappings folder
    """

    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(extract_location)

    print("Extracted file to previous folder")


def report_recursive(dcmp, output_file):
    f = open(output_file, "w")
    for name in dcmp.diff_files:
        before = open(f"{dcmp.left}/{name}").readlines()
        after = open(f"{dcmp.right}/{name}").readlines()
        diff_lines = []
        for line in difflib.unified_diff(before, after, lineterm="", n=0):
            for prefix in ("---", "+++", "@@", "-}", "+}"):
                if line.startswith(prefix):
                    break
            else:
                diff_lines.append(line)

        if len(diff_lines) > 0:

            f.write(
                "Difference in file %s found in %s and %s\n"
                % (name, dcmp.left, dcmp.right)
            )
            for diff_line in diff_lines:
                f.write(diff_line)

    for name in dcmp.left_only:
        f.write("Old file %s deleted in %s\n" % (name, dcmp.left))
    for name in dcmp.right_only:
        f.write("New file %s found in %s\n" % (name, dcmp.right))
    for sub_dcmp in dcmp.subdirs.values():
        report_recursive(sub_dcmp, output_file)

    f.close()


def get_latest_version(bucket, key, client):
    versions = client.list_object_versions(Prefix=key, Bucket=bucket)
    for version in [*versions["Versions"]]:
        if version["IsLatest"]:
            return version["VersionId"]


@click.command()
@click.option("--role", default="operator")
def main(role):
    dirs_to_zip = [
        f"{shared_path}/mapping_spreadsheet",
        f"{mappings_path}/mapping_definitions",
    ]
    zip_file = f"{zip_file_prefix}{ext}"
    zip_dir(dirs_to_zip, zip_file)
    s3_file_path = f"{s3_folder}/{zip_file_prefix}{ext}"
    s3 = assume_aws_session(account, role).client("s3")
    zip_dir(dirs_to_zip, zip_file)
    upload_file(bucket_name, zip_file, s3, s3_file_path)
    print(get_latest_version(bucket_name, s3_file_path, s3))


if __name__ == "__main__":

    main()
