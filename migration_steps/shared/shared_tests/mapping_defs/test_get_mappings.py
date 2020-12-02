import json
import os
from helpers import get_mapping_dict


def test_get_mapping_dict():

    result = get_mapping_dict(
        file_name="test_client_persons_mapping", stage_name="transform_casrec"
    )

    dirname = os.path.dirname(__file__)
    file_path = os.path.join(
        dirname, f"expected_results/test_client_persons_expected.json"
    )

    with open(file_path) as expected_json:
        expected_result = json.load(expected_json)

        assert result == expected_result
