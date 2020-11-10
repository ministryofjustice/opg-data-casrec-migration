from pytest_cases import parametrize_with_cases

from data_tests.cases import cases_cases_simple
from data_tests.clients import cases_clients_simple
from data_tests.helpers import (
    get_data_from_query,
    get_merge_col_data_as_list,
    merge_source_and_transformed_df,
    SAMPLE_PERCENTAGE,
)

list_of_test_cases = [cases_clients_simple]


@parametrize_with_cases(
    ("defaults", "source_query"), cases=list_of_test_cases, has_tag="default",
)
def test_default_values(get_config, defaults, source_query):

    # print(f"source_query: {source_query}")

    config = get_config

    source_sample_df = get_data_from_query(
        query=source_query, config=config, sample=True
    )

    print(source_sample_df.to_markdown())

    assert source_sample_df.shape[0] > 0

    print(f"Checking {source_sample_df.shape[0]} rows of data ({SAMPLE_PERCENTAGE}%) ")
    assert source_sample_df.shape[0] > 0
    for k, v in defaults.items():
        matches = source_sample_df[k].str.contains(str(v))
        total_matches = matches.sum()
        success = total_matches == source_sample_df.shape[0]
        print(f"checking {k} == {v}.... {'OK' if success else 'oh no'} ")
        assert success

        # match = source_sample_df[k] == v

        #
        # assert match is True
