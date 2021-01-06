from pytest_cases import parametrize_with_cases

from data_tests.conftest import (
    list_of_test_cases,
    add_to_tested_list,
)
from data_tests.helpers import get_data_from_query
import logging

log = logging.getLogger("root")


@parametrize_with_cases(
    ("defaults", "source_query", "module_name"),
    cases=list_of_test_cases,
    has_tag="default",
)
def test_default_values(test_config, defaults, source_query, module_name):
    log.debug(f"module_name: {module_name}")

    config = test_config

    add_to_tested_list(
        module_name=module_name, tested_fields=[x for x in defaults.keys()]
    )

    source_sample_df = get_data_from_query(
        query=source_query, config=config, sample=True
    )

    assert source_sample_df.shape[0] > 0

    log.debug(
        f"Checking {source_sample_df.shape[0]} rows of data ({config.SAMPLE_PERCENTAGE}%) from table: {module_name} "
    )
    assert source_sample_df.shape[0] > 0
    for k, v in defaults.items():
        source_sample_df["compare_col"] = v
        # matches = source_sample_df[k].str.contains(str(v))
        matches = source_sample_df[k] == source_sample_df["compare_col"]
        total_matches = matches.sum()
        success = total_matches == source_sample_df.shape[0]
        log.log(
            config.VERBOSE,
            f"checking {k} == {v}...." f" {'OK' if success else 'oh no'} ",
        )
        assert success
