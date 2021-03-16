import os
import json


def get_current_directory():
    dirname = os.path.dirname(__file__)
    return dirname


def get_entities_with_details():

    entity_details = {}

    dirname = get_current_directory()
    file_path = os.path.join(dirname, f"mapping_definitions")

    for json_file in os.listdir(file_path):
        mapping_file_name = json_file[:-5]
        json_file_path = os.path.join(file_path, json_file)
        if os.path.isfile(json_file_path):
            with open(json_file_path, "r") as definition_json:
                def_dict = json.load(definition_json)
                for field, details in def_dict.items():
                    entity = details["sirius_details"]["entity"]
                    if entity != "":
                        if entity in entity_details:
                            entity_details[entity]["details"]["mapping_files"].append(
                                mapping_file_name
                            ) if mapping_file_name not in entity_details[entity][
                                "details"
                            ][
                                "mapping_files"
                            ] else ""
                            sirius_table_name = details["sirius_details"]["table_name"]
                            entity_details[entity]["details"]["sirius_tables"].append(
                                sirius_table_name
                            ) if sirius_table_name not in entity_details[entity][
                                "details"
                            ][
                                "sirius_tables"
                            ] else ""
                        else:
                            entity_details[entity] = {
                                "details": {
                                    "mapping_files": [mapping_file_name],
                                    "sirius_tables": [
                                        details["sirius_details"]["table_name"]
                                    ],
                                }
                            }

    return entity_details


def check_stage_progress(stage, item_name):

    dirname = get_current_directory()
    file_path = os.path.join(dirname, f"progress")

    with open(f"{file_path}/{stage}_progress.json") as progress_file:
        data = progress_file.read()
        progress_data = json.loads(data)

    complete = 0
    for item in item_name:
        if item in progress_data:
            complete += 1
    complete_percentage = int(round(complete / len(item_name), 2) * 100)

    return complete_percentage


def check_mapping_progress(mapping_files):

    dirname = get_current_directory()
    file_path = os.path.join(dirname, f"mapping_definitions/summary")

    with open(f"{file_path}/mapping_progress_summary.json") as progress_file:
        data = progress_file.read()
        progress_data = json.loads(data)

    sheet_data = progress_data["worksheets"]

    total_rows = 0
    total_mapped = 0
    for file in mapping_files:
        file = file[:-8]
        total_rows += sheet_data[file]["total_rows"]
        total_mapped += sheet_data[file]["total_mapped"]

    complete_percentage = int(round(total_mapped / total_rows, 2) * 100)

    return complete_percentage


def get_entity_progress(entity_list):
    entity_list_with_progress = entity_list

    for entity_name, entity_details in entity_list.items():

        mapping_progress = check_mapping_progress(
            mapping_files=entity_details["details"]["mapping_files"]
        )

        transform_progress = check_stage_progress(
            stage="transform", item_name=entity_details["details"]["mapping_files"]
        )
        staging_progress = check_stage_progress(
            stage="load_to_staging",
            item_name=entity_details["details"]["sirius_tables"],
        )
        sirius_progress = check_stage_progress(
            stage="load_to_sirius", item_name=entity_details["details"]["sirius_tables"]
        )
        progress = {
            "mapping": mapping_progress,
            "transform": transform_progress,
            "staging": staging_progress,
            "sirius": sirius_progress,
        }

        entity_list_with_progress[entity_name]["progress"] = progress

    create_progress_json(entity_list_with_progress)
    return entity_list_with_progress


def create_progress_json(progress_dict):
    dirname = get_current_directory()
    file_path = os.path.join(dirname, f"progress")

    with open(f"{file_path}/entity_progress.json", "w+") as progress_file:
        progress_file.write(json.dumps(progress_dict, indent=4))
