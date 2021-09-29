import boto3
import json
import os
import click
import time
from botocore.credentials import RefreshableCredentials
from botocore.session import get_session
from datetime import datetime, timedelta


class TaskRunner:
    role = "breakglass"
    account = {
        "development": "288342028542",
        "preproduction": "492687888235",
        "qa": "492687888235",
    }
    sts_client = ""
    region = ""
    auto_refresh_session_task_runner = ""
    auto_refresh_session_logs = ""
    wait_time = 0

    def __init__(self, environment, region, role):
        self.role = role
        self.environment = environment
        self.region = region
        self.wait_time = 0
        self.start_time = int(datetime.now().timestamp())
        self.sts_client = boto3.client("sts")
        self.role_name = f"arn:aws:iam::{self.account[environment]}:role/{role}"

    def set_log_group(self, log_group):
        self.log_group = log_group

    def print_from_logs(self):
        query = (
            "fields @timestamp, @logStream, @message | sort @timestamp asc | limit 1000"
        )

        start_time = self.start_time
        end_time = int((datetime.today() + timedelta(days=1)).timestamp())

        start_query_response = self.auto_refresh_session_logs.start_query(
            logGroupName=self.log_group,
            startTime=start_time,
            endTime=end_time,
            queryString=query,
        )
        query_id = start_query_response["queryId"]
        time.sleep(1)
        response = self.auto_refresh_session_logs.get_query_results(queryId=query_id)

        log_records = []
        for fields in response["results"]:
            log_record = {
                "timestamp": fields[0]["value"],
                "logStream": fields[1]["value"],
                "message": fields[2]["value"],
                "ptr": fields[3]["value"],
            }
            log_records.append(log_record)

        for log_record in log_records:
            print(
                f"{log_record['timestamp']} - {log_record['logStream']}: {log_record['message']}"
            )

    def refresh_creds(self):
        "Refresh tokens by calling assume_role again"
        params = {
            "RoleArn": self.role_name,
            "RoleSessionName": "step_function_session",
            "DurationSeconds": 900,
        }

        response = self.sts_client.assume_role(**params).get("Credentials")
        credentials = {
            "access_key": response.get("AccessKeyId"),
            "secret_key": response.get("SecretAccessKey"),
            "token": response.get("SessionToken"),
            "expiry_time": response.get("Expiration").isoformat(),
        }
        return credentials

    def create_session_runner(self):
        session_credentials = RefreshableCredentials.create_from_metadata(
            metadata=self.refresh_creds(),
            refresh_using=self.refresh_creds,
            method="sts-assume-role",
        )
        session = get_session()
        session._credentials = session_credentials
        session.set_config_variable("region", self.region)
        autorefresh_session = boto3.Session(botocore_session=session)
        self.auto_refresh_session_task_runner = autorefresh_session.client(
            "ecs", region_name=self.region
        )

    def create_session_logs(self):
        session_credentials = RefreshableCredentials.create_from_metadata(
            metadata=self.refresh_creds(),
            refresh_using=self.refresh_creds,
            method="sts-assume-role",
        )
        session = get_session()
        session._credentials = session_credentials
        session.set_config_variable("region", self.region)
        autorefresh_session = boto3.Session(botocore_session=session)
        self.auto_refresh_session_logs = autorefresh_session.client(
            "logs", region_name=self.region
        )

    def run_ecs_task(self, task_identifier, task_name, command):
        with open(
            "/terraform/environment/terraform.output_casrec_migration.json"
        ) as json_file:
            data = json.load(json_file)

        response = self.auto_refresh_session_task_runner.run_task(
            cluster=data["Tasks"]["value"][task_identifier]["Cluster"],
            launchType="FARGATE",
            taskDefinition=data["Tasks"]["value"][task_identifier]["TaskDefinition"],
            count=1,
            platformVersion="LATEST",
            networkConfiguration={
                "awsvpcConfiguration": {
                    "subnets": data["Tasks"]["value"][task_identifier][
                        "NetworkConfiguration"
                    ]["AwsvpcConfiguration"]["Subnets"],
                    "securityGroups": data["Tasks"]["value"][task_identifier][
                        "NetworkConfiguration"
                    ]["AwsvpcConfiguration"]["SecurityGroups"],
                }
            },
            overrides={
                "containerOverrides": [{"name": task_name, "command": command}],
            },
        )
        return response

    def wait_for_task_to_stop(self, cluster_arn, task_arn):
        waiter = self.auto_refresh_session_task_runner.get_waiter("tasks_stopped")
        response = waiter.wait(
            cluster=cluster_arn,
            tasks=[task_arn,],
            include=["TAGS",],
            WaiterConfig={"Delay": 6, "MaxAttempts": 100},
        )

        return response

    def get_stop_exit_code(self, cluster_arn, task_arn):
        response = self.auto_refresh_session_task_runner.describe_tasks(
            cluster=cluster_arn, tasks=[task_arn,], include=["TAGS",],
        )
        exit_code = response["tasks"][0]["stopCode"]
        stop_reason = response["tasks"][0]["stoppedReason"]

        return exit_code, stop_reason


@click.command()
@click.option("-i", "--task_identifier", default="preparation")
@click.option("-n", "--task_name", default="etl0")
@click.option("-c", "--task_command", default="validation/validate.sh")
@click.option("-l", "--log_group", default="casrec-migration-development")
def main(task_identifier, task_name, task_command, log_group):
    environment = os.getenv("ENVIRONMENT")
    region = "eu-west-1"
    role = "breakglass"
    task_runner = TaskRunner(environment, region, role)
    task_runner.set_log_group(log_group)
    task_runner.create_session_runner()
    task_runner.create_session_logs()

    task_list = task_command.split(",")

    response = task_runner.run_ecs_task(task_identifier, task_name, task_list)

    task_arn = response["tasks"][0]["containers"][0]["taskArn"]
    cluster_arn = response["tasks"][0]["clusterArn"]
    print(f"Running against task: {task_arn}")
    print(f"Running against cluster: {cluster_arn}")
    task_runner.wait_for_task_to_stop(cluster_arn, task_arn)
    code, reason = task_runner.get_stop_exit_code(cluster_arn, task_arn)

    if code == "EssentialContainerExited":
        print("Container ran correctly - checking logs...")
        time.sleep(120)
        task_runner.set_log_group(log_group)
        task_runner.print_from_logs()
    else:
        print(f"{code} - {reason}")
        print("There was a problem with your run. Check ECS")


if __name__ == "__main__":
    main()
