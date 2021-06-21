import boto3
import click


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


@click.command()
@click.option("--role", default="operator")
@click.option("--environment", default="development")
def main(role, environment):
    account = {"development": "288342028542", "preproduction": "492687888235"}
    session = assume_aws_session(account[environment], role)
    ssm = session.client("ssm", region_name="eu-west-1")
    parameter = ssm.get_parameter(Name=f"{environment}-allowed-entities")
    print(parameter["Parameter"]["Value"])


if __name__ == "__main__":
    main()