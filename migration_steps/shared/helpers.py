import os
import json


def log_title(message: str) -> str:
    total_length = 100
    padded_word = f" {message} "
    left_filler_length = round((total_length - len(padded_word)) / 2)
    right_filler_length = total_length - len(padded_word) - left_filler_length

    left_filler = "=" * left_filler_length
    right_filler = "=" * right_filler_length

    log_string = left_filler + padded_word.upper() + right_filler

    return log_string


def get_mapping_dict(file_name: str) -> str:
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, f"mapping_definitions/{file_name}.json")

    with open(file_path) as mapping_json:
        mapping_dict = json.load(mapping_json)

    return {k: v["transform_casrec"] for k, v in mapping_dict.items()}


def get_lookup_dict(file_name: str) -> str:
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(
        dirname, f"mapping_definitions/lookups" f"/{file_name}.json"
    )

    with open(file_path) as lookup_json:
        lookup_dict = json.load(lookup_json)

        return {k: v["sirius_mapping"] for k, v in lookup_dict.items()}
