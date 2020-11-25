import os
import json
from typing import Dict, List


def log_title(message: str) -> str:
    total_length = 100
    padded_word = f" {message} "
    left_filler_length = round((total_length - len(padded_word)) / 2)
    right_filler_length = total_length - len(padded_word) - left_filler_length

    left_filler = "=" * left_filler_length
    right_filler = "=" * right_filler_length

    log_string = left_filler + padded_word.upper() + right_filler

    return log_string


def get_mapping_dict(file_name: str, stage_name: str) -> Dict:
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, f"mapping_definitions/{file_name}.json")

    with open(file_path) as mapping_json:
        mapping_dict = json.load(mapping_json)

    return {k: v[stage_name] for k, v in mapping_dict.items()}


def get_lookup_dict(file_name: str) -> Dict:
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(
        dirname, f"mapping_definitions/lookups" f"/{file_name}.json"
    )

    with open(file_path) as lookup_json:
        lookup_dict = json.load(lookup_json)

        return {k: v["sirius_mapping"] for k, v in lookup_dict.items()}


def get_all_mapped_fields(
    complete: bool = True, include_keys: bool = False
) -> Dict[str, List[str]]:
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, f"mapping_definitions")

    all_mapping_dicts = {}

    for json_file in os.listdir(file_path):
        json_file_path = os.path.join(file_path, json_file)
        if os.path.isfile(json_file_path):
            with open(json_file_path, "r") as definition_json:
                def_dict = json.load(definition_json)

                key_name = json_file.replace("_mapping.json", "")
                if include_keys:
                    all_mapping_dicts[key_name] = [
                        k
                        for k, v in def_dict.items()
                        if v["mapping_status"]["is_complete"] is complete
                    ]
                else:
                    all_mapping_dicts[key_name] = [
                        k
                        for k, v in def_dict.items()
                        if v["mapping_status"]["is_complete"] is complete
                        and v["sirius_details"]["is_pk"] is not True
                        and len(v["sirius_details"]["fk_parents"]) == 0
                    ]

    return all_mapping_dicts
