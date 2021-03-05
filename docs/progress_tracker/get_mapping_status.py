import json

path = (
    "migration_steps/shared/mapping_definitions/summary/mapping_progress_summary.json"
)


def get_total_progress():
    with open(path, "r") as summary_file:
        summary_dict = json.load(summary_file)

    return summary_dict["total"]["fields"]["percentage_complete"]
