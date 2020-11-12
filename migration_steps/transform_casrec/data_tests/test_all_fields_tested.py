import deepdiff
import pytest
import os
import json


@pytest.mark.xfail(reason="not all fields implemented yet")
@pytest.mark.last
def test_all_fields():
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, f"./field_list")
    file_name = "tested_fields.json"

    try:
        with open(f"{file_path}/{file_name}", "r") as fields_json:
            fields_dict = json.load(fields_json)
    except IOError:
        fields_dict = {}

    expected_fields = {}
    definitions_dir = os.path.join(dirname, f"mapping_definitions")
    for json_file in os.listdir(definitions_dir):
        json_file_path = os.path.join(definitions_dir, json_file)
        if os.path.isfile(json_file_path):
            with open(json_file_path, "r") as definition_json:
                def_dict = json.load(definition_json)

                key_name = json_file.replace("_mapping.json", "")
                expected_fields[key_name] = [
                    k for k, v in def_dict.items() if v["is_complete"] is True
                ]

    errors = {}
    for k in expected_fields.keys():
        assert k in fields_dict

        diff = list(set(expected_fields[k]) - set(fields_dict[k]))
        if len(diff) > 0:
            errors[k] = diff

    print(
        ("\n").join(
            [f"{len(v)} errors in {k}: {(', ').join(v)}" for k, v in errors.items()]
        )
    )

    os.remove(f"{file_path}/{file_name}")
    assert sum([len(x) for x in errors.values()]) == 0
