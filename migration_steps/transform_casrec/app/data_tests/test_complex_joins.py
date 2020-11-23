from pytest_cases import parametrize_with_cases

from data_tests.conftest import (
    list_of_test_cases,
    SAMPLE_PERCENTAGE,
)
from data_tests.helpers import (
    get_data_from_query,
    get_merge_col_data_as_list,
    merge_source_and_transformed_df,
)


@parametrize_with_cases(
    (
        "module_name",
        "source_query",
        "transformed_query",
        "merge_columns",
        "match_columns",
    ),
    cases=list_of_test_cases,
    has_tag="many_to_one_join",
)
def test_complex_joins(
    test_config,
    module_name,
    source_query,
    transformed_query,
    merge_columns,
    match_columns,
):
    print(f"module_name: {module_name}")

    config = test_config

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

    print(f"Checking {result_df.shape[0]} rows of data ({SAMPLE_PERCENTAGE}%) ")
    assert result_df.shape[0] > 0
    for k, v in match_columns.items():
        match = result_df[k].equals(result_df[v])
        print(f"checking {k} == {v}.... {'OK' if match is True else 'oh no'} ")

        assert match is True
