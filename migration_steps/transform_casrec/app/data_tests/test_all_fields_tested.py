import pytest
import os
import json
import logging

from helpers import get_all_mapped_fields
log = logging.getLogger("root")


@pytest.mark.parametrize(
    "complete_status",
    [
        True,
        pytest.param(
            False, marks=pytest.mark.xfail(reason="not all fields mapped yet")
        ),
    ],
)
@pytest.mark.last
def test_all_fields(complete_status):
    dirname = os.path.dirname(__file__)
    file_name = "tested_fields.json"

    try:
        with open(f"{dirname}/{file_name}", "r") as fields_json:
            fields_dict = json.load(fields_json)
    except IOError:
        fields_dict = {}

    expected_fields = get_all_mapped_fields(complete=complete_status)
    errors = {}

    for k in expected_fields.keys():

        if k in fields_dict:
            diff = list(set(expected_fields[k]) - set(fields_dict[k]))
            if len(diff) > 0:
                errors[k] = diff

    log.log(
        config.VERBOSE,
        ("\n").join(
            [
                f"{len(v)} untested fields in table {k}: {(', ').join(v)}"
                for k, v in errors.items()
            ]
        ),
    )

    assert sum([len(x) for x in errors.values()]) == 0
