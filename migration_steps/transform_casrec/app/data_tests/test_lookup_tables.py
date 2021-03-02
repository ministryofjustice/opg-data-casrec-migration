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
import logging


from helpers import get_lookup_dict

log = logging.getLogger("root")


@parametrize_with_cases(
    (
        "lookup_fields",
        "merge_columns",
        "source_query",
        "transformed_query",
        "module_name",
    ),
    cases=list_of_test_cases,
    has_tag="lookups",
)
def test_map_lookup_tables(
    test_config,
    lookup_fields,
    merge_columns,
    source_query,
    transformed_query,
    module_name,
):
    print(f"module_name: {module_name}")

    add_to_tested_list(
        module_name=module_name,
        tested_fields=[x for x in lookup_fields.keys()]
        + [merge_columns["transformed"]],
    )

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

    log.debug(
        f"Checking {result_df.shape[0]} rows of data ({config.SAMPLE_PERCENTAGE}%) from table: {module_name} "
    )
    assert result_df.shape[0] > 0
    for k, v in lookup_fields.items():
        for i, j in v.items():

            lookup_dict = get_lookup_dict(file_name=j.lower())

            match = (
                result_df[i].map(lookup_dict).fillna("").equals(result_df[k].fillna(""))
            )

            print(
                f"checking {k} == {i}...."
                f""
                f" {'OK' if match is True else 'oh no'} ",
            )

            assert match is True
