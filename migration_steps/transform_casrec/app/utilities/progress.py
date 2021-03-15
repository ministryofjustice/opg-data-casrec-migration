import json
from pathlib import Path


def update_progress(mapping_files_used):
    mapping_files_used = json.dumps(list(mapping_files_used))

    root_path = Path(__file__).parents[1]

    with open(f"{root_path}/progress.json", "w+") as file:
        file.write(mapping_files_used)
