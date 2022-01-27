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


def get_latest_per_page(image_tag, response, latest=None, image=None):
    for images in response["imageDetails"]:
        if "imageTags" in images:
            for each_image in images["imageTags"]:
                if image_tag in each_image:
                    if latest is None:
                        latest = images["imagePushedAt"]
                        image = each_image
                    elif images["imagePushedAt"] > latest:
                        latest = images["imagePushedAt"]
                        image = each_image
    return latest, image


def get_next_token(response):
    if "nextToken" in response:
        next_token = response["nextToken"]
    else:
        next_token = None

    return next_token


@click.command()
@click.option("--role", default="operator")
@click.option("--image_tag", default="main")
def main(role, image_tag):
    account = "311462405659"
    region = "eu-west-1"
    ecr_session = assume_aws_session(account, role)
    client = ecr_session.client("ecr", region_name=region)

    response = client.describe_images(repositoryName="casrec-migration/etl0")
    next_token = get_next_token(response)
    latest_time, image_id = get_latest_per_page(image_tag, response)

    while next_token is not None:
        response = client.describe_images(
            repositoryName="casrec-migration/etl0", nextToken=next_token
        )
        next_token = get_next_token(response)
        latest_time, image_id = get_latest_per_page(
            image_tag, response, latest_time, image_id
        )

    print(image_id)


if __name__ == "__main__":
    main()
