from pytest_cases import parametrize_with_cases

from data_tests.cases import cases_cases_simple
from data_tests.clients import cases_clients_simple
from data_tests.helpers import (
    get_data_from_query,
    get_merge_col_data_as_list,
    merge_source_and_transformed_df,
)

list_of_cases = [cases_clients_simple]


@parametrize_with_cases(
    ("simple_matches", "merge_columns", "source_query", "transformed_query"),
    cases=list_of_cases,
    has_tag="simple",
)
def test_simple_transformations(
    get_config, simple_matches, merge_columns, source_query, transformed_query
):

    print(f"source_query: {source_query}")
    print(f"transformed_query: {transformed_query}")

    config = get_config

    source_sample_df = get_data_from_query(
        query=source_query, config=config, sort_col=merge_columns["source"], sample=True
    )

    assert source_sample_df.shape[0] > 0

    sample_cases = get_merge_col_data_as_list(
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
        transformed_df[merge_columns["transformed"]].isin(sample_cases)
    ]

    result_df = merge_source_and_transformed_df(
        source_df=source_sample_df,
        transformed_df=transformed_sample_df,
        merge_columns=merge_columns,
    )

    print(f"Checking {result_df.shape[0]} rows of data")
    assert result_df.shape[0] > 0
    for k, v in simple_matches.items():
        assert result_df[k].equals(result_df[v]) is True
