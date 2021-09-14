import time
import boto3
import os
import shutil
import click
import pandas as pd
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))


def operator_session(environment):
    account = {"development": "288342028542", "preproduction": "492687888235"}
    client = boto3.client("sts")

    role_to_assume = f"arn:aws:iam::{account[environment]}:role/operator"
    response = client.assume_role(
        RoleArn=role_to_assume, RoleSessionName="assumed_role"
    )

    session = boto3.Session(
        aws_access_key_id=response["Credentials"]["AccessKeyId"],
        aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
        aws_session_token=response["Credentials"]["SessionToken"],
    )

    return session


def download_list_of_files(bucket_name, s3, local_data_path, s3_folder):
    print("Starting download of files")
    resp = s3.list_objects_v2(Bucket=bucket_name)
    files_in_bucket = []

    for obj in resp["Contents"]:
        file_and_folder = obj["Key"]
        folder = file_and_folder.split("/")[0]
        file = file_and_folder.split("/")[1]
        dl_file_location = str(local_data_path) + "/" + file
        if folder == s3_folder and file.endswith(".csv"):
            s3.download_file(bucket_name, file_and_folder, dl_file_location)
            print(file_and_folder)
            files_in_bucket.append(file_and_folder)

    print(f"Total files returned: {len(files_in_bucket)}")


def clear_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))
    print("Cleared folder")


def csv_formatting(path, file_name):
    full_file_name = f"{path}/{file_name}"
    with open(full_file_name, "r") as file:
        file_data = file.read()

    # Replace things we need to replace
    file_data = file_data.replace(" 00:00:00", "")

    # Write the file out again
    with open(full_file_name, "w") as file:
        file.write(file_data)


def merge_edge_cases_locally(edge_data_path, local_data_path):
    for filename in os.listdir(edge_data_path):
        csv_formatting(edge_data_path, filename)
        edge_data = pd.read_csv(edge_data_path / filename, dtype=str)

        edge_data = edge_data.replace("NaT", "")
        edge_data = edge_data.replace(" 00:00:00", "")

        original_csv = local_data_path / filename.replace("_anon", "")
        max_id = pd.read_csv(original_csv)["rct"].max()

        edge_data[edge_data.columns[0]] = edge_data[edge_data.columns[0]].astype(int)
        edge_data[edge_data.columns[0]] += max_id + 1
        edge_data.insert(1, "rct", edge_data[edge_data.columns[0]], True)

        if filename == "pat_anon.csv":
            edge_data.insert(2, "by", "MIG", True)
        elif filename in [
            "order_anon.csv",
            "deputy_anon.csv",
            "deputyship_anon.csv",
            "remarks_anon.csv",
            "deputy_address_anon.csv",
        ]:
            edge_data.insert(2, "create", "2021-06-01", True)

        print(f"Adding data to {original_csv}")

        add_new_lines(original_csv)
        edge_data.to_csv(original_csv, mode="a", header=False, index=False)


def add_new_lines(csv_path):
    with open(csv_path, "r") as f:
        f.seek(0, 2)
        f.seek(f.tell() - 2, 0)
        elems = f.read()
        for elem in elems:
            last_elem = elem
        if last_elem != "\n":
            with open(csv_path, "a") as f2:
                f2.write("\n")


@click.command()
@click.option("-e", "--environment", default="development")
def main(environment):
    csv_dir_suffix = os.getenv("CSV_DIR_SUFFIX")
    bucket = f"casrec-migration-{environment}"
    s3_session = operator_session(environment)
    s3 = s3_session.client("s3")
    local_data_path = current_path / csv_dir_suffix

    # envcheck
    # todo not sure this covers all envs?
    if environment == "development":
        clear_folder(local_data_path)
        download_list_of_files(bucket, s3, local_data_path, "anon")
        print("Finished syncing data from dev environment")
    elif environment == "preproduction":
        edge_data_path = local_data_path / "../edge_cases_csvs"
        download_list_of_files(bucket, s3, edge_data_path, "edge_cases_csvs")
        merge_edge_cases_locally(edge_data_path, local_data_path)
        print("Finished adding edge cases to your data set")


if __name__ == "__main__":
    t = time.process_time()
    main()
    print(f"Total time: {round(time.process_time() - t, 2)}")
