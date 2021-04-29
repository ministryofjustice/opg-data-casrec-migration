import boto3
import click
import os
import time
import json
from botocore.credentials import RefreshableCredentials
from botocore.session import get_session


class StepFunctionRunner:
    role_name = ""
    sts_client = ""
    region = ""
    auto_refresh_session_step_func = ""
    sf_arn = ""
    execution_arn = ""
    wait_time = 0

    def __init__(self, role_name, sts_client, region):
        self.role_name = role_name
        self.sts_client = sts_client
        self.region = region
        self.wait_time = 0

    def step_function_arn(self, step_function_name):
        state_machines = self.auto_refresh_session_step_func.list_state_machines()
        for machine in state_machines["stateMachines"]:
            if machine["name"] == step_function_name:
                print(f'Setting ARN to: {machine["stateMachineArn"]}')
                self.sf_arn = machine["stateMachineArn"]
            else:
                print("No state machine of given name exists")
                os._exit(1)

    def step_function_running_wait_for(self, wait_for):
        secs = 30
        executions = self.auto_refresh_session_step_func.list_executions(
            stateMachineArn=self.sf_arn, statusFilter="RUNNING"
        )
        if len(executions["executions"]) > 0 and self.wait_time < wait_for:
            time.sleep(secs)
            self.wait_time += secs
            print(f"Waited for {self.wait_time} seconds. Timeout is {wait_for}")
            self.step_function_running_wait_for(wait_for)
        elif self.wait_time > 1800:
            print("Timeout.. something is wrong. Check the step function")
            os._exit()
        else:
            print("Ready to run step function")

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

    def create_session(self):
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


@click.command()
@click.option("--role", default="operator")
@click.option("--account", default="288342028542")
@click.option("--wait_for", default="1800")
@click.option("--no_reload", default="false")
@click.option("--environment", default="development")
def main(role, account, wait_for, no_reload, environment):
    region = "eu-west-1"
    sf_name = f"casrec-mig-state-machine-{environment}"
    role_to_assume = f"arn:aws:iam::{account}:role/{role}"
    base_client = boto3.client("sts")

    step_function_runner = StepFunctionRunner(role_to_assume, base_client, region)

    step_function_runner.create_session()
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
