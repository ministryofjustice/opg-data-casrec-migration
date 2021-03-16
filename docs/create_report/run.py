import os
import sys
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../migration_steps/shared")

from jinja2 import Environment, FileSystemLoader
import os


from generate_progress_file import get_entity_progress, get_entities_with_details


entity_list = get_entities_with_details()
progress_details = get_entity_progress(entity_list=entity_list)


def generate_report():

    root = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(root, "templates")
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("progress_tracker.html")

    filename = os.path.join(root, "progress_tracker.html")
    with open(filename, "w+") as fh:
        fh.write(template.render(progress=progress_details))

    p = Path(os.path.join(root, "progress_tracker.html")).absolute()
    parent_dir = p.parents[1]
    destination = parent_dir / "external_docs"
    p.rename(destination / p.name)


generate_report()
