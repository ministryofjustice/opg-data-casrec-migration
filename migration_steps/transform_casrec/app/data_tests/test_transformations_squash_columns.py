from ast import literal_eval

from pytest_cases import parametrize_with_cases

from data_tests.conftest import (
    list_of_test_cases,
    add_to_tested_list,
)
from data_tests.helpers import (
    get_data_from_query,
    get_merge_col_data_as_list,
    merge_source_and_transformed_df,
)
import pandas as pd
import logging
import pytest

log = logging.getLogger("root")


@pytest.mark.xfail(reason="dates need formatting properly")
@parametrize_with_cases(
    (
        "squash_columns_fields",
        "source_query",
        "transformed_query",
        "merge_columns",
        "module_name",
    ),
    cases=list_of_test_cases,
    has_tag="squash_columns",
)
def test_squash_columns(
    test_config,
    squash_columns_fields,
    source_query,
    transformed_query,
    merge_columns,
    module_name,
):
    log.debug(f"module_name: {module_name}")

    config = test_config
    add_to_tested_list(
        module_name=module_name, tested_fields=[x for x in squash_columns_fields.keys()]
    )

    source_sample_df = get_data_from_query(
        query=source_query, config=config, sort_col=merge_columns["source"], sample=True
    )

    assert source_sample_df.shape[0] > 0

    sample_caserefs = get_merge_col_data_as_list(
        df=source_sample_df, column_name=merge_columns["source"]
    )

    transformed_df = get_data_from_query(
        query=transformed_query,
        config=config,
        sort_col=merge_columns["transformed"],
        sample=False,
    )

    assert transformed_df.shape[0] > 0

    transformed_sample_df = transformed_df[
        transformed_df[merge_columns["transformed"]].isin(sample_caserefs)
    ]

    result_df = merge_source_and_transformed_df(
        source_df=source_sample_df,
        transformed_df=transformed_sample_df,
        merge_columns=merge_columns,
    )

    log.debug(
        f"Checking {result_df.shape[0]} rows of data ({config.SAMPLE_PERCENTAGE}%) from table: {module_name} "
    )

    assert result_df.shape[0] > 0

    for k, v in squash_columns_fields.items():
        for i, j in enumerate(v):
            split_result = result_df[k].map(literal_eval).apply(pd.Series)
            match = result_df[j].equals(split_result[i])

            log.log(
                config.VERBOSE,
                f"checking {j} == {k}:{i}...."
                f" {'OK' if match is True else 'oh no'} ",
            )

            assert match is True
