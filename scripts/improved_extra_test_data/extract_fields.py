# This is a handy mini script for debugging what sort of things might cause errors using sqlalchemy.
import os
import sys
import json
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../migration_steps/shared")

from dotenv import load_dotenv

# set config
current_path = Path(os.path.dirname(os.path.realpath(__file__)))
env_path = current_path / "../../migration_steps/.env"
load_dotenv(dotenv_path=env_path)
evironment = os.environ.get("ENVIRONMENT")

file_path = str(current_path) + "/../../migration_steps/shared/mapping_definitions"

for json_file in os.listdir(file_path):
    mapping_file_name = json_file[:-5]
    json_file_path = os.path.join(file_path, json_file)
    if os.path.isfile(json_file_path):
        with open(json_file_path, "r") as definition_json:
            def_dict = json.load(definition_json)

            for field, details in def_dict.items():
                print(field)
                print(json.dumps(details, indent=4))
