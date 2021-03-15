import json
import logging
from pathlib import Path
import os

log = logging.getLogger("root")


def update_progress(module_name, completed_items):
    log.debug(f"Updating progress file for {module_name}")

    completed_items = json.dumps(list(completed_items))

    dirname = os.path.dirname(__file__)

    with open(f"{dirname}/progress/{module_name}_progress.json", "w+") as file:
        file.write(completed_items)
