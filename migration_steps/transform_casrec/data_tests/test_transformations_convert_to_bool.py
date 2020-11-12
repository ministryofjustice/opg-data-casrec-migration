from pytest_cases import parametrize_with_cases

from data_tests.conftest import (
    list_of_test_cases,
    SAMPLE_PERCENTAGE,
    add_to_tested_list,
)
from data_tests.helpers import (
    get_data_from_query,
    get_merge_col_data_as_list,
    merge_source_and_transformed_df,
)


@parametrize_with_cases(
    (
        "convert_to_bool_fields",
        "source_query",
        "transformed_query",
        "merge_columns",
        "module_name",
    ),
    cases=list_of_test_cases,
    has_tag="convert_to_bool",
)
def test_convert_to_bool(
    get_config,
    convert_to_bool_fields,
    source_query,
    transformed_query,
    merge_columns,
    module_name,
):

    config = get_config
    add_to_tested_list(
        module_name=module_name,
        tested_fields=[y for x in convert_to_bool_fields.values() for y in x],
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

    print(f"Checking {result_df.shape[0]} rows of data ({SAMPLE_PERCENTAGE}%) ")
    assert result_df.shape[0] > 0
    for k, v in convert_to_bool_fields.items():
        for i in v:
            true_values = ["true", "True", "t", "T", "1", "1.0"]

            true_rows = result_df[result_df[k].isin(true_values)]
            total_true_rows = true_rows.shape[0]
            true_matches = true_rows[i]
            total_true_matches = true_matches.shape[0]

            t_match = total_true_rows == total_true_matches
            print(
                f"checking True: {total_true_rows} {k} =="
                f" {total_true_matches} "
                f"{i}.... {'OK' if t_match is True else 'oh no'} "
            )
            assert t_match

            false_rows = result_df[~result_df[k].isin(true_values)]
            total_false_rows = false_rows.shape[0]
            false_matches = false_rows[i]
            total_false_matches = false_matches.shape[0]

            f_match = total_false_rows == total_false_matches

            print(
                f"checking False: {total_false_rows} {k} =="
                f" {total_false_matches} "
                f"{i}.... {'OK' if f_match is True else 'oh no'} "
            )
            assert f_match
