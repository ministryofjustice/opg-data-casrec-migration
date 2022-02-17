import boto3
import click
import time
from botocore.credentials import RefreshableCredentials
from botocore.session import get_session
from datetime import datetime, timedelta


class TaskRunner:
    account = {
        "development": "288342028542",
        "preproduction": "492687888235",
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
        self.log_group = None
        self.start_time = int(datetime.now().timestamp())
        self.sts_client = boto3.client("sts")
        self.role_name = f"arn:aws:iam::{self.account[environment]}:role/{role}"

    def set_log_group(self, log_group):
        self.log_group = log_group

    def print_from_logs(self, start_time, finish_time):
        query = "fields @timestamp, @logStream, @message | sort @timestamp asc | limit 10000"

        start = datetime.strptime(start_time, "%Y/%m/%d %H:%M:%S")
        finish = datetime.strptime(finish_time, "%Y/%m/%d %H:%M:%S")

        seconds_between_start_finish = (finish - start).total_seconds()
        # rounds up to next hour
        hours_between_start_finish = int(
            int(seconds_between_start_finish // 3600)
            + int(seconds_between_start_finish % 3600 > 0)
        )

        print(f"{hours_between_start_finish} hours time span")
        log_records = []
        timed_log_records = []
        for i in range(0, hours_between_start_finish):
            print(f"Running chunk: {i} of {hours_between_start_finish}")
            hours_added = timedelta(hours=i)
            one_hour = timedelta(hours=1)
            start_time_chunk = start + hours_added
            end_time_chunk = start_time_chunk + one_hour

            print(f"Querying logs between {start_time_chunk} and {end_time_chunk}")

            start_query_response = self.auto_refresh_session_logs.start_query(
                logGroupName=self.log_group,
                startTime=int(start_time_chunk.timestamp()),
                endTime=int(end_time_chunk.timestamp()),
                queryString=query,
            )
            query_id = start_query_response["queryId"]
            time.sleep(1)
            response = self.auto_refresh_session_logs.get_query_results(
                queryId=query_id
            )

            results_gathered = len(response["results"])
            print(f"Gathered {results_gathered} records from this set")

            if results_gathered > 10000:
                print(
                    f"WARNING -- Too many results in this time frame - Consider shortening chunk timeframe"
                )

            for fields in response["results"]:
                log_record = {
                    "timestamp": fields[0]["value"],
                    "logStream": fields[1]["value"],
                    "message": fields[2]["value"],
                    "ptr": fields[3]["value"],
                }
                log_records.append(log_record)

        previous_log_record = None
        for log_record in log_records:
            if previous_log_record is None:
                previous_log_record = log_record

            previous_timestamp = datetime.strptime(
                previous_log_record["timestamp"], "%Y-%m-%d %H:%M:%S.%f"
            )
            current_timestamp = datetime.strptime(
                log_record["timestamp"], "%Y-%m-%d %H:%M:%S.%f"
            )

            time_diff = (current_timestamp - previous_timestamp).total_seconds()

            timed_log_record = {
                "timeTaken": f"{round(time_diff, 2)}",
                "logStream": previous_log_record["logStream"],
                "message": previous_log_record["message"],
            }

            previous_log_record = log_record

            timed_log_records.append(timed_log_record)

        sorted_timed_log_records = sorted(
            timed_log_records, key=lambda d: (float(d["timeTaken"]) * -1)
        )

        print(f"\n====== Longest running records ======\n")

        count = 0
        for log_record in sorted_timed_log_records:
            print(
                f'{round(float(log_record["timeTaken"]) / 60, 2)}mins - {log_record["message"]}'
            )
            if count > 20:
                break
            count += 1

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


@click.command()
@click.option("-l", "--log_group", default="casrec-migration-development")
@click.option("-e", "--environment", default="development")
@click.option("-s", "--start_time", default="2022/01/01 17:05:00")
@click.option("-f", "--finish_time", default="2022/01/01 22:40:00")
def main(log_group, environment, start_time, finish_time):
    region = "eu-west-1"
    role = "operator"
    task_runner = TaskRunner(environment, region, role)
    task_runner.set_log_group(log_group)
    task_runner.create_session_logs()
    task_runner.print_from_logs(start_time, finish_time)


"""
The log parser allows you to select logs from a single log group between certain datetimes and see which
are the worst performing areas of the sequential process.
This is useful for sequential runs like this migration as we're simply interested in the time difference
between log messages.
This should give us a good indication of where the process is taking a long time.
"""
if __name__ == "__main__":
    main()
