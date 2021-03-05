from jinja2 import Environment, FileSystemLoader
import os
import json

from get_mapping_status import get_total_progress

root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, "templates")
env = Environment(loader=FileSystemLoader(templates_dir))
template = env.get_template("index.html")


progress_details = [
    {"stage": "mapped", "percentage": f"{get_total_progress()}%"},
    {"stage": "transformed", "percentage": "20%"},
    {"stage": "integrated", "percentage": "18%"},
    {"stage": "migrated", "percentage": "4%"},
]


filename = os.path.join(root, "index.html")
with open(filename, "w") as fh:
    fh.write(template.render(progress=progress_details))
