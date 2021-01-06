import logging

from pytest_cases import parametrize_with_cases

from data_tests.conftest import list_of_test_cases
from data_tests.helpers import get_data_from_query

log = logging.getLogger("root")


@parametrize_with_cases(
    ("source_query", "transformed_query", "module_name",),
    cases=list_of_test_cases,
    has_tag="row_count",
)
def test_row_counts(
    test_config, source_query, transformed_query, module_name,
):
    log.debug(f"module_name: {module_name}")

    config = test_config

    source_sample_df = get_data_from_query(
        query=source_query, config=config, sample=False
    )

    assert source_sample_df.shape[0] > 0

    transformed_df = get_data_from_query(
        query=transformed_query, config=config, sample=False,
    )

    assert transformed_df.shape[0] > 0

    match = source_sample_df.shape[0] == transformed_df.shape[0]

    log.log(
        config.VERBOSE,
        f"checking row count for {module_name}.... "
        f"{'OK' if match is True else 'oh no'} ",
    )

    assert match is True
