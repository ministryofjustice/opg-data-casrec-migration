import json
import os

import pandas as pd

from data_tests.conftest import SAMPLE_PERCENTAGE


def get_data_from_query(
    query, config, sort_col=None, sample=False, sample_percentage=SAMPLE_PERCENTAGE
):
    df = pd.read_sql_query(query, config.connection_string)

    if sample:
        df = df.sample(frac=sample_percentage / 100, replace=False, random_state=1)

    if sort_col:
        return df.sort_values(by=[sort_col])
    else:
        return df


def get_merge_col_data_as_list(df, column_name):

    col = df[column_name].to_list()
    return col


def merge_source_and_transformed_df(source_df, transformed_df, merge_columns):
    return source_df.merge(
        transformed_df,
        how="inner",
        left_on=merge_columns["source"],
        right_on=merge_columns["transformed"],
    )


def get_lookup_dict(file_name: str) -> str:

    file_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            f"mapping_definitions/" f"lookups/{file_name}.json",
        )
    )

    with open(file_path) as lookup_json:
        lookup_dict = json.load(lookup_json)

        better_lookup_dict = {k: v["sirius_mapping"] for k, v in lookup_dict.items()}

    return better_lookup_dict
