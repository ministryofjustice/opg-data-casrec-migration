import boto3
import click
import os
import time
import json
from botocore.credentials import RefreshableCredentials
from botocore.session import get_session
from datetime import datetime, timedelta


def to_datetime(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")


class StepFunctionRunner:
    role_name = ""
    sts_client = ""
    region = ""
    auto_refresh_session_step_func = ""
    auto_refresh_session_logs = ""
    sf_arn = ""
    execution_arn = ""
    wait_time = 0
    previous_pointers = []
    latest_timestamp = ""
    log_group = ""

    def __init__(self, role_name, sts_client, region):
        self.role_name = role_name
        self.sts_client = sts_client
        self.region = region
        self.wait_time = 0
        self.latest_timestamp = datetime.fromtimestamp(
            int((datetime.now() - timedelta(hours=12)).timestamp())
        )

    def step_function_arn(self, step_function_name):
        state_machines = self.auto_refresh_session_step_func.list_state_machines()
        for machine in state_machines["stateMachines"]:
            if machine["name"] == step_function_name:
                print(f'Setting ARN to: {machine["stateMachineArn"]}')
                self.sf_arn = machine["stateMachineArn"]
                return machine["stateMachineArn"]
        print("No state machine of given name exists")
        os._exit(1)

    def step_function_running_wait_for(self, wait_for):
        secs = 30
        executions = self.auto_refresh_session_step_func.list_executions(
            stateMachineArn=self.sf_arn, statusFilter="RUNNING"
        )
        self.print_from_logs()
        if len(executions["executions"]) > 0 and self.wait_time < wait_for:
            time.sleep(secs)
            self.wait_time += secs
            print(f"Waited for {self.wait_time} seconds. Timeout is {wait_for}")
            self.step_function_running_wait_for(wait_for)
        elif self.wait_time > wait_for:
            print("Timeout.. something is wrong. Check the step function")
            os._exit()
        else:
            print("Ready to run step function")

    def set_log_group(self, log_group):
        self.log_group = log_group

    def print_from_logs(self):
        query = (
            "fields @timestamp, @logStream, @message | sort @timestamp asc | limit 1000"
        )

        start_time = int((datetime.now() - timedelta(minutes=5)).timestamp())
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
            if (
                (fields[0]["field"] == "@timestamp")
                and (to_datetime(fields[0]["value"]) >= self.latest_timestamp)
                and (fields[3]["value"] not in self.previous_pointers)
            ):
                log_record = {
                    "timestamp": fields[0]["value"],
                    "logStream": fields[1]["value"],
                    "message": fields[2]["value"],
                    "ptr": fields[3]["value"],
                }
                log_records.append(log_record)
                self.latest_timestamp = to_datetime(log_record["timestamp"])

        for log_record in log_records:
            print(
                f"{log_record['timestamp']} - {log_record['logStream']}: {log_record['message']}"
            )
        if len(log_records) > 0:
            self.previous_pointers = []
            for ptr in log_records:
                self.previous_pointers.append(ptr["ptr"])

    def run_step_function(self, no_reload):
        if no_reload == "true":
            print("Starting step function in 'no reload' mode")
            input_json = {
                "prep": ["prepare/prepare.sh", "-i", "casrec_csv"],
                "load1": ["python3", "app.py", "--skip_load=true"],
                "load2": ["python3", "app.py", "--skip_load=true"],
                "load3": ["python3", "app.py", "--skip_load=true"],
                "load4": ["python3", "app.py", "--skip_load=true"],
            }
        else:
            print("Starting step function in 'reload' (normal) mode")
            input_json = {
                "prep": ["prepare/prepare.sh"],
                "load1": ["python3", "app.py", "--skip_load=false", "--delay=0"],
                "load2": ["python3", "app.py", "--skip_load=false", "--delay=2"],
                "load3": ["python3", "app.py", "--skip_load=false", "--delay=3"],
                "load4": ["python3", "app.py", "--skip_load=false", "--delay=4"],
            }
        response = self.auto_refresh_session_step_func.start_execution(
            stateMachineArn=self.sf_arn, input=str(json.dumps(input_json))
        )
        return response

    def last_step_function_status_response(self):
        response = self.auto_refresh_session_step_func.describe_execution(
            executionArn=self.execution_arn
        )
        return response["status"]

    def get_execution_arn(self):
        executions = self.auto_refresh_session_step_func.list_executions(
            stateMachineArn=self.sf_arn, statusFilter="RUNNING"
        )

        for execution in executions["executions"]:
            self.execution_arn = execution["executionArn"]

    def refresh_creds(self):
        " Refresh tokens by calling assume_role again "
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

    def create_session_step(self):
        session_credentials = RefreshableCredentials.create_from_metadata(
            metadata=self.refresh_creds(),
            refresh_using=self.refresh_creds,
            method="sts-assume-role",
        )
        session = get_session()
        session._credentials = session_credentials
        session.set_config_variable("region", self.region)
        autorefresh_session = boto3.Session(botocore_session=session)
        self.auto_refresh_session_step_func = autorefresh_session.client(
            "stepfunctions", region_name=self.region
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


@click.command()
@click.option("--role", default="operator")
@click.option("--account", default="288342028542")
@click.option("--wait_for", default="1800")
@click.option("--no_reload", default="false")
@click.option("--workspace", default="development")
def main(role, account, wait_for, no_reload, workspace):
    region = "eu-west-1"
    sf_name = f"casrec-mig-state-machine-{workspace}"
    log_group = f"casrec-migration-{workspace}"
    role_to_assume = f"arn:aws:iam::{account}:role/{role}"
    base_client = boto3.client("sts")

    step_function_runner = StepFunctionRunner(role_to_assume, base_client, region)

    step_function_runner.set_log_group(log_group)
    step_function_runner.create_session_step()
    step_function_runner.create_session_logs()
    step_function_runner.step_function_arn(sf_name)
    step_function_runner.step_function_running_wait_for(int(wait_for))
    response = step_function_runner.run_step_function(no_reload)

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        print("Step function started correctly")
    else:
        print(response["ResponseMetadata"])

    time.sleep(5)

    step_function_runner.get_execution_arn()
    step_function_runner.step_function_running_wait_for(int(wait_for))

    if step_function_runner.last_step_function_status_response() == "SUCCEEDED":
        print("Last step successful")
    else:
        print("Step function did not execute successfully. Go check!")
        os._exit(1)


if __name__ == "__main__":
    main()
