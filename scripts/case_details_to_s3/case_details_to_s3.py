import boto3
import json
import os
import click


def operator_session(environment):

    account = {"development": "288342028542", "preproduction": "492687888235"}
    client = boto3.client("sts")

    role_to_assume = f"arn:aws:iam::{account[environment]}:role/migration-pull-case-role.{environment}"
    response = client.assume_role(
        RoleArn=role_to_assume, RoleSessionName="assumed_role"
    )

    session = boto3.Session(
        aws_access_key_id=response["Credentials"]["AccessKeyId"],
        aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
        aws_session_token=response["Credentials"]["SessionToken"],
    )

    return session


def run_ecs_task(client, caserecnumber):
    with open("/terraform/terraform.output_casrec_migration.json") as json_file:
        data = json.load(json_file)

    response = client.run_task(
        cluster=data["Tasks"]["value"]["pull-case"]["Cluster"],
        launchType="FARGATE",
        taskDefinition=data["Tasks"]["value"]["pull-case"]["TaskDefinition"],
        count=1,
        platformVersion="LATEST",
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": data["Tasks"]["value"]["pull-case"]["NetworkConfiguration"][
                    "AwsvpcConfiguration"
                ]["Subnets"],
                "securityGroups": data["Tasks"]["value"]["pull-case"][
                    "NetworkConfiguration"
                ]["AwsvpcConfiguration"]["SecurityGroups"],
            }
        },
        overrides={
            "containerOverrides": [
                {
                    "name": "etl0",
                    "command": [
                        "python3",
                        "prepare/case_details_to_s3/app/app.py",
                        "-c",
                        caserecnumber,
                    ],
                },
            ],
        },
    )
    return response


def wait_for_task_to_stop(client, cluster_arn, task_arn):
    waiter = client.get_waiter("tasks_stopped")
    response = waiter.wait(
        cluster=cluster_arn,
        tasks=[
            task_arn,
        ],
        include=[
            "TAGS",
        ],
        WaiterConfig={"Delay": 6, "MaxAttempts": 100},
    )

    return response


def get_stop_exit_code(client, cluster_arn, task_arn):
    response = client.describe_tasks(
        cluster=cluster_arn,
        tasks=[
            task_arn,
        ],
        include=[
            "TAGS",
        ],
    )
    exit_code = response["tasks"][0]["stopCode"]
    stop_reason = response["tasks"][0]["stoppedReason"]

    return exit_code, stop_reason


@click.command()
@click.option("-c", "--caserecnumber", default="10000037")
def main(caserecnumber):
    environment = os.getenv("ENVIRONMENT")
    op_session = operator_session(environment)
    client = op_session.client("ecs", region_name="eu-west-1")
    response = run_ecs_task(client, caserecnumber)
    task_arn = response["tasks"][0]["containers"][0]["taskArn"]
    cluster_arn = response["tasks"][0]["clusterArn"]
    print(f"Running against task: {task_arn}")
    print(f"Running against cluster: {cluster_arn}")
    wait_for_task_to_stop(client, cluster_arn, task_arn)
    code, reason = get_stop_exit_code(client, cluster_arn, task_arn)

    if code == "EssentialContainerExited":
        print("Container ran correctly - checking logs...")
        # Add logging here...
    else:
        print(f"{code} - {reason}")
        print("There was a problem with your run. Check ECS")


if __name__ == "__main__":
    main()
