import logging
import os
import re

import pandas as pd
import helpers

from transform_data.lookup_tables import map_lookup_tables
from utilities.generate_source_query import additional_cols, format_additional_col_alias

log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")

config = helpers.get_config(env=environment)


def conditional_lookup(
    final_col: str,
    lookup_col: str,
    data_col: str,
    lookup_file_name: str,
    df: pd.DataFrame,
) -> pd.DataFrame:

    print("IDHEWQDUWEOHFOUEHFUEOHEWFOUHEWQFOUHEWFOUEHWQFUOWHQOFUHWUOEFHEWQOUFWEQOUF")

    print(df.columns.values)

    log.log(
        config.VERBOSE,
        f"Doing conditional lookup using final_col: {final_col}, lookup_col: {lookup_col}, data_col: {data_col}, "
        f"lookup_file_name: {lookup_file_name}",
    )

    temp_col = "mapping_col"
    print(lookup_col)
    lookup_col = format_additional_col_alias(lookup_col)

    print(lookup_col)

    pattern = re.compile(f"^{data_col}$|^{data_col}\s[0-9]+$|^{data_col}\s$")
    data_col = list(filter(pattern.match, df.columns.tolist()))[0]

    lookup_dict = helpers.get_lookup_dict(lookup_file_name)
    print(lookup_dict)

    print(df[lookup_col])

    df[temp_col] = df[lookup_col].map(lookup_dict)
    df[temp_col] = df[temp_col].fillna("")

    def blah(x):
        print(
            f"data_col_value: {x[data_col]}, temp_col: {x[temp_col]}, data_col: {data_col}, lookup: {x[lookup_col]}"
        )
        return x[data_col] if x[temp_col] == data_col else None

    df[final_col] = df.apply(lambda x: blah(x), axis=1)

    df = df.drop(columns=[temp_col, data_col])

    log.log(config.VERBOSE, f"Dataframe size after conditional lookup: {len(df)}")

    return df
