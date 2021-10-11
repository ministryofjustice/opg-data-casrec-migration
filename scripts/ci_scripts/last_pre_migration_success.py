import boto3
import click
import sys


class StepFunctionSuccessChecker:
    def __init__(self):
        self.session = ""
        self.sf_client = boto3.client("sts")
        self.region = "eu-west-1"
        self.sf_arn = ""
        self.execution_arn = ""

    def set_step_function_arn(self, step_function_name):
        state_machines = self.sf_client.list_state_machines()
        for machine in state_machines["stateMachines"]:
            if machine["name"] == step_function_name:
                print(f'Setting ARN to: {machine["stateMachineArn"]}')
                self.sf_arn = machine["stateMachineArn"]
                return machine["stateMachineArn"]
        print("No state machine of given name exists")
        sys.exit(1)

    def get_latest_execution_status(self):
        executions = self.sf_client.list_executions(stateMachineArn=self.sf_arn)

        return executions["executions"][0]["status"]

    def assume_aws_session(self, account, role):
        """
        Assume an AWS session so that we can access AWS resources as that account
        """

        client = boto3.client("sts")
        role_to_assume = f"arn:aws:iam::{account}:role/{role}"
        response = client.assume_role(
            RoleArn=role_to_assume, RoleSessionName="assumed_role"
        )

        self.session = boto3.Session(
            aws_access_key_id=response["Credentials"]["AccessKeyId"],
            aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
            aws_session_token=response["Credentials"]["SessionToken"],
        )

        self.sf_client = self.session.client("stepfunctions", region_name=self.region)


@click.command()
@click.option("--role", default="operator")
def main(role):
    account_id = "492687888235"
    sf_name = "casrec-mig-state-machine-preproduction"

    sf_success_checker = StepFunctionSuccessChecker()
    sf_success_checker.assume_aws_session(account_id, role)
    sf_success_checker.set_step_function_arn(sf_name)
    status = sf_success_checker.get_latest_execution_status()

    if status == "SUCCEEDED":
        print("Last PreProd Run successful - Carrying on with PreQA run")
    else:
        print(
            "Last PreProd Run unsuccessful - Failing PreQA run to minimise risk to environment"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
