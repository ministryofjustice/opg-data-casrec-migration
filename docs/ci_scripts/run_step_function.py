import boto3
import click
import sys
import time
import json


def assume_aws_session(account, role):
    """
    Assume an AWS session so that we can access AWS resources as that account
    """

    client = boto3.client("sts")
    account_id = client.get_caller_identity()["Account"]
    print(f"Current users account: {account_id}")

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


def step_function_arn(client, step_function_name):
    state_machines = client.list_state_machines()
    for machine in state_machines["stateMachines"]:
        if machine["name"] == step_function_name:
            return machine["stateMachineArn"]
        else:
            print("No state machine of given name exists")
            os._exit(1)


def step_function_running_wait_for(client, step_function_arn, wait_for, wait_time=0):
    secs = 10
    executions = client.list_executions(
        stateMachineArn=step_function_arn, statusFilter="RUNNING"
    )
    if len(executions["executions"]) > 0 and wait_time < wait_for:
        time.sleep(secs)
        wait_time += secs
        print(f"Waited for {wait_time} seconds")
        step_function_running_wait_for(
            client, step_function_arn, wait_for, wait_time=wait_time
        )
    elif wait_time > 1800:
        print("Timeout.. something is wrong. Check the step function")
        os._exit()
    else:
        print("Ready to run step function")


def run_step_function(client, step_function_arn, no_reload):
    if no_reload == "true":
        input_json = {
            "prep": ["prepare/prepare.sh", "-i", "casrec_csv"],
            "load1": ["python3", "app.py", "--skip_load=true"],
            "load2": ["python3", "app.py", "--skip_load=true"],
            "load3": ["python3", "app.py", "--skip_load=true"],
            "load4": ["python3", "app.py", "--skip_load=true"],
        }
    else:
        input_json = {
            "prep": ["prepare/prepare.sh"],
            "load1": ["python3", "app.py", "--skip_load=false", "--delay=0"],
            "load2": ["python3", "app.py", "--skip_load=false", "--delay=2"],
            "load3": ["python3", "app.py", "--skip_load=false", "--delay=3"],
            "load4": ["python3", "app.py", "--skip_load=false", "--delay=4"],
        }
    response = client.start_execution(
        stateMachineArn=step_function_arn, input=str(json.dumps(input_json))
    )
    return response


def last_step_function_status_response(client, execution_arn):
    response = client.describe_execution(executionArn=execution_arn)
    return response["status"]


def get_execution_arn(client, step_function_arn):
    executions = client.list_executions(
        stateMachineArn=step_function_arn, statusFilter="RUNNING"
    )

    for execution in executions["executions"]:
        return execution["executionArn"]


@click.command()
@click.option("--role", default="operator")
@click.option("--account", default="288342028542")
@click.option("--wait_for", default="1800")
@click.option("--no_reload", default="false")
def main(role, account, wait_for, no_reload):
    region = "eu-west-1"
    sf_name = "casrec-mig-state-machine"
    s3_session = assume_aws_session(account, role)
    client = s3_session.client("stepfunctions", region_name=region)

    arn = step_function_arn(client, sf_name)

    step_function_running_wait_for(client, arn, int(wait_for))

    response = run_step_function(client, arn, no_reload)

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        print("Step function started correctly")
    else:
        print(response["ResponseMetadata"])

    time.sleep(5)

    execution_arn = get_execution_arn(client, arn)
    step_function_running_wait_for(client, arn, int(wait_for))

    if last_step_function_status_response(client, execution_arn) == "SUCCEEDED":
        print("Last step successful")
    else:
        print("Step function did not execute successfully. Go check!")
        os._exit(1)


if __name__ == "__main__":
    main()
