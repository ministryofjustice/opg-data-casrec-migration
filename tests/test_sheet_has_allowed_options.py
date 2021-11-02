import json

import pytest

from app.mapping_all_sheets import Mapping
from tests.conftest import expected_options
from tests.conftest import mapping_doc
from tests.conftest import test_file_paths


@pytest.mark.parametrize("option", ["requires_transformation", "calculated"])
def test_options(option):

    mapping = Mapping(
        mapping_doc_name=mapping_doc, new_format=True, file_paths=test_file_paths
    )
    mapping.generate_json_files()

    with open(expected_options, "r") as expected_json:
        expected_data = expected_json.read()
        expected_dict = json.loads(expected_data)

    expected_single_option = expected_dict[option]

    with open(
        f"{test_file_paths['mapping_definitions_output']}/rainbows_mapping.json", "r"
    ) as result_json:
        result_data = result_json.read()
        result_dict = json.loads(result_data)

    used_options = [
        x["transform_casrec"][option]
        for x in result_dict.values()
        if x["transform_casrec"][option] != ""
    ]

    assert all(x in expected_single_option for x in used_options)
