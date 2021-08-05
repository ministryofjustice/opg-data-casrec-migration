import datetime
import time
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


def write_to_ddb(dynamodb_client, workspace_name):
    year = datetime.datetime.today() + datetime.timedelta(days=365)
    expiry_date_time = int(time.mktime(year.timetuple()))

    try:
        dynamodb_client.put_item(
            TableName="WorkspaceCleanup",
            Item={
                "WorkspaceName": {"S": workspace_name},
                "ExpiresTTL": {"N": str(expiry_date_time)},
            },
        )
        return True
    except Exception as e:
        print("Exception: ", e)
        return False


def query_ddb(dynamodb_resource, workspace_name):
    table = dynamodb_resource.Table("WorkspaceCleanup")
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key("WorkspaceName").eq(
            workspace_name
        )
    )
    return response["Items"]


@click.command()
@click.option("--role", default="operator")
def main(role):
    account = "288342028542"
    region = "eu-west-1"
    workspace = "casmigrate"
    assumed_session = assume_aws_session(account, role)
    dynamodb_client = assumed_session.client("dynamodb", region_name=region)
    dynamodb_resource = assumed_session.resource("dynamodb", region_name=region)
    print(f"Executing update to TTL value for {workspace}")
    write_to_ddb(dynamodb_client, workspace)
    query_response = query_ddb(dynamodb_resource, workspace)
    print(query_response)


if __name__ == "__main__":
    main()
