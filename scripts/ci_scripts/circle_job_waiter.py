import requests
import json
import click
import time
import os


def get_running_jobs(
    circle_builds_token,
    circle_project_username,
    circle_project_reponame,
    current_workflow_id,
):
    running_jobs_url = f"https://circleci.com/api/v1.1/project/github/{circle_project_username}/{circle_project_reponame}?circle-token={circle_builds_token}"
    response = requests.get(running_jobs_url)
    running_jobs = []
    if response.status_code == 200:
        running_jobs_json = json.loads(response.text)

        for job in running_jobs_json:
            if job["status"] == "queued" or job["status"] == "running":
                if job["workflows"]["workflow_id"] != current_workflow_id:
                    if (
                        "pre" not in job["workflows"]["job_name"]
                        and "qa" not in job["workflows"]["job_name"]
                    ):
                        print(
                            f"Job: \"{job['workflows']['job_name']}\", Status: \"{job['status']}\""
                        )
                        running_jobs.append(job["workflows"]["job_name"])
        return running_jobs
    else:
        print(f"API call to circle failed with status code: {response.status_code}")
        return running_jobs


@click.command()
@click.option("--circle_builds_token", default=None)
@click.option("--circle_project_username", default=None)
@click.option("--circle_project_reponame", default=None)
def main(circle_builds_token, circle_project_username, circle_project_reponame):
    if "CIRCLE_WORKFLOW_ID" in os.environ:
        current_workflow_id = os.environ["CIRCLE_WORKFLOW_ID"]
    else:
        current_workflow_id = "None"

    time_taken = 0
    secs = 10
    all_clear_count = 0
    while all_clear_count < 3:
        if (
            len(
                get_running_jobs(
                    circle_builds_token,
                    circle_project_username,
                    circle_project_reponame,
                    current_workflow_id,
                )
            )
            > 0
        ):
            time.sleep(secs)
            time_taken += secs
            print(f"Waited {time_taken} seconds for previous job to finish")
        else:
            if time_taken < 10:
                print("No jobs running")
                continue
            else:
                all_clear_count += 1
                print(f"No jobs running - Check {all_clear_count} of 3")

    print("Ready to kick off our job")


if __name__ == "__main__":
    main()
