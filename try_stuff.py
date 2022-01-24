import boto3


def assume_aws_session(account, role):
    """
    Assume an AWS session so that we can access AWS resources as that account
    """

    client = boto3.client("sts")

    role_to_assume = f"arn:aws:iam::{account}:role/{role}"
    response = client.assume_role(
        RoleArn=role_to_assume, RoleSessionName="assumed_role"
    )

    assumed_session = boto3.Session(
        aws_access_key_id=response["Credentials"]["AccessKeyId"],
        aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
        aws_session_token=response["Credentials"]["SessionToken"],
    )

    return assumed_session


def main():
    role = "operator"
    account = "492687888235"
    bucket_name = "casrec-migration-preproduction"
    s3 = assume_aws_session(account, role).client("s3")
    print(s3.list_objects_v2(Bucket=bucket_name))


if __name__ == "__main__":

    main()
