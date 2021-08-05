import json
import logging


import os
import sys
from pathlib import Path


current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../shared")

import helpers

log = logging.getLogger("root")

environment = os.environ.get("ENVIRONMENT")
config = helpers.get_config(env=environment)


def update_progress(module_name, completed_items):
    if "generate_progress" not in config.enabled_feature_flags(env=environment):
        return False

    log.debug(f"Updating progress file for {module_name}")

    completed_items = json.dumps(list(completed_items))

    dirname = os.path.dirname(__file__)

    with open(f"{dirname}/progress/{module_name}_progress.json", "w+") as file:
        file.write(completed_items)

    log.debug(
        f"Number of mapping docs used in module {module_name}: {len(completed_items)}"
    )
