from pytest_cases import parametrize_with_cases

from data_tests.conftest import (
    list_of_test_cases,
    add_to_tested_list,
)
from data_tests.helpers import get_data_from_query
import logging

log = logging.getLogger("root")


@parametrize_with_cases(
    ("calculated_fields", "source_query", "module_name"),
    cases=list_of_test_cases,
    has_tag="calculated",
)
def test_calculated_values(test_config, calculated_fields, source_query, module_name):
    log.debug(f"module_name: {module_name}")
    print(f"module_name: {module_name}")

    # log.debug(f"source_query: {source_query}")

    config = test_config

    add_to_tested_list(
        module_name=module_name, tested_fields=[x for x in calculated_fields.keys()]
    )

    source_sample_df = get_data_from_query(
        query=source_query, config=config, sample=True
    )

    # print(source_sample_df.to_markdown())
    source_sample_df.info()
    assert source_sample_df.shape[0] > 0

    log.debug(
        f"Checking {source_sample_df.shape[0]} rows of data ("
        f"{config.SAMPLE_PERCENTAGE}%) from table: {module_name}"
    )
    assert source_sample_df.shape[0] > 0
    for k, v in calculated_fields.items():
        print(f"k: {k}")
        print(f"v: {v}")
        source_sample_df["compare_col"] = v
        matches = source_sample_df[k] == source_sample_df["compare_col"]
        print(f"source_sample_df[k]: {source_sample_df[k]}")
        print(f'source_sample_df["compare_col"]: {source_sample_df["compare_col"]}')

        total_matches = matches.sum()
        success = total_matches == source_sample_df.shape[0]
        log.log(
            config.VERBOSE,
            f"checking {k} == {v}.... " f"{'OK' if success else 'oh no'} ",
        )
        assert success
