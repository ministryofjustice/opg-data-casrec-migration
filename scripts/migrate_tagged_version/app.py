import boto3
import click


class MigrateTaggedVersion:
    def __init__(self):
        self.role = "operator"
        self.sirius_account = "288342028542"
        self.management_account = "311462405659"
        self.region = "eu-west-1"
        self.assumed_session = ""
        self.list_of_images = []
        self.describe_images_response = []
        self.next_token = None
        self.tag_filter = "all"

    def assume_aws_session(self, account):
        """
        Assume an AWS session so that we can access AWS resources as that account
        """

        client = boto3.client("sts")

        role_to_assume = f"arn:aws:iam::{account}:role/{self.role}"
        response = client.assume_role(
            RoleArn=role_to_assume, RoleSessionName="assumed_role"
        )

        self.assumed_session = boto3.Session(
            aws_access_key_id=response["Credentials"]["AccessKeyId"],
            aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
            aws_session_token=response["Credentials"]["SessionToken"],
        )

    def get_workflow_secret(self):
        self.assume_aws_session(self.sirius_account)
        client = self.assumed_session.client("secretsmanager", region_name=self.region)
        secret = client.get_secret_value(
            SecretId="development/migration_circleci_token"
        )
        print(secret["SecretString"])

    def append_to_list_of_images_per_page(self):
        for image in self.describe_images_response["imageDetails"]:
            if "imageTags" in image:
                image_tag_and_date = {
                    "image_tags": image["imageTags"],
                    "date": image["imagePushedAt"].strftime("%Y-%m-%d %H:%M:%S"),
                }
                if self.tag_filter == "all":
                    self.list_of_images.append(image_tag_and_date)
                else:
                    if any(
                        self.tag_filter in string
                        for string in image_tag_and_date["image_tags"]
                    ):
                        self.list_of_images.append(image_tag_and_date)

    def get_next_token(self):
        if "nextToken" in self.describe_images_response:
            self.next_token = self.describe_images_response["nextToken"]
        else:
            self.next_token = None

    def get_page_of_tagged_builds(self, client):
        repo_name = "casrec-migration/etl0"
        if self.next_token is not None:
            self.describe_images_response = client.describe_images(
                repositoryName=repo_name, nextToken=self.next_token
            )
        else:
            self.describe_images_response = client.describe_images(
                repositoryName=repo_name
            )
        self.get_next_token()
        self.append_to_list_of_images_per_page()

    def get_list_of_tagged_builds(self, tag_filter):
        self.tag_filter = tag_filter
        if self.tag_filter != "all":
            self.tag_filter = self.tag_filter + "-"
        self.assume_aws_session(self.management_account)
        client = self.assumed_session.client("ecr", region_name=self.region)

        self.get_page_of_tagged_builds(client)
        while self.next_token is not None:
            self.get_page_of_tagged_builds(client)

        sorted_image_list = sorted(self.list_of_images, key=lambda x: x["date"].lower())
        latest_images_list = sorted_image_list[-10:]

        for i in latest_images_list:
            print(i)


@click.command()
@click.option("--cmd", default="get_secret_key")
@click.option("--tag_filter", default="qa-")
def main(cmd, tag_filter):
    migrate = MigrateTaggedVersion()
    if cmd == "get_secret_key":
        migrate.get_workflow_secret()
    elif cmd == "list_of_tagged_builds":
        migrate.get_list_of_tagged_builds(tag_filter)


if __name__ == "__main__":
    main()
