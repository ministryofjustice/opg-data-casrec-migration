import pytest
import os
import json


@pytest.mark.parametrize("complete_status", [True, False])
@pytest.mark.xfail(reason="not all fields implemented yet")
@pytest.mark.last
def test_all_fields(complete_status):
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, f"./field_list")
    file_name = "tested_fields.json"

    try:
        with open(f"{file_path}/{file_name}", "r") as fields_json:
            fields_dict = json.load(fields_json)
    except IOError:
        fields_dict = {}

    expected_fields = {}
    definitions_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "app/mapping_definitions")
    )

    for json_file in os.listdir(definitions_dir):
        json_file_path = os.path.join(definitions_dir, json_file)
        if os.path.isfile(json_file_path):
            with open(json_file_path, "r") as definition_json:
                def_dict = json.load(definition_json)

                key_name = json_file.replace("_mapping.json", "")
                expected_fields[key_name] = [
                    k
                    for k, v in def_dict.items()
                    if v["mapping_status"]["is_complete"] is complete_status
                    and v["sirius_details"]["is_pk"] is not True
                    and len(v["sirius_details"]["fk_parents"]) == 0
                ]
    errors = {}

    for k in expected_fields.keys():

        if k in fields_dict:
            diff = list(set(expected_fields[k]) - set(fields_dict[k]))
            if len(diff) > 0:
                errors[k] = diff
            print(f"module_name: {k} with {len(diff)} errors")

    print(
        ("\n").join(
            [f"{len(v)} errors in {k}: {(', ').join(v)}" for k, v in errors.items()]
        )
    )

    assert sum([len(x) for x in errors.values()]) == 0
