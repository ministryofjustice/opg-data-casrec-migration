from pytest_cases import parametrize_with_cases

from data_tests.conftest import (
    list_of_test_cases,
    SAMPLE_PERCENTAGE,
    add_to_tested_list,
)
from data_tests.helpers import (
    get_data_from_query,
    get_merge_col_data_as_list,
)


@parametrize_with_cases(
    (
        "join_columns",
        "merge_columns",
        "fk_child_query",
        "fk_parent_query",
        "module_name",
    ),
    cases=list_of_test_cases,
    has_tag="one_to_one_joins",
)
def test_one_to_one_joins(
    get_config,
    join_columns,
    merge_columns,
    fk_child_query,
    fk_parent_query,
    module_name,
):
    print(f"module_name: {module_name}")
    print(f"[x for x in join_columns.values()]: {[x for x in join_columns.keys()]}")

    add_to_tested_list(
        module_name=module_name, tested_fields=[x for x in join_columns.keys()]
    )

    config = get_config

    fk_child_df = get_data_from_query(query=fk_child_query, config=config, sample=True,)

    sample_caserefs = get_merge_col_data_as_list(
        df=fk_child_df, column_name=merge_columns["fk_child"]
    )

    fk_parent_df = get_data_from_query(
        query=fk_parent_query,
        config=config,
        sort_col=merge_columns["fk_parent"],
        sample=False,
    )
    fk_parent_sample_df = fk_parent_df[
        fk_parent_df[merge_columns["fk_parent"]].isin(sample_caserefs)
    ]

    fk_child_id_list = fk_child_df[[k for k in join_columns][0]].tolist()
    fk_child_id_list = [int(x) for x in fk_child_id_list]

    fk_parent_id_list = fk_parent_sample_df[
        [y for x in join_columns.values() for y in x.values()][0]
    ].tolist()
    fk_parent_id_list = [int(x) for x in fk_parent_id_list]

    print(f"Checking {fk_parent_df.shape[0]} rows of data ({SAMPLE_PERCENTAGE}%) ")
    success = set(fk_child_id_list) == set(fk_parent_id_list)
    print(
        f"checking {[k for k in join_columns][0]} == "
        f"{[y for x in join_columns.values() for y in x.values()][0]}.... "
        f"{'OK' if success is True else 'oh no'} "
    )
    assert success is True
