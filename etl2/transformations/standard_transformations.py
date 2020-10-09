import json
import random
import pandas as pd


def do_simple_remap(simple_mapping_dict, source_table_name, source_data):
    simple_column_remap = [
        {v["alias"]: k}
        for k, v in simple_mapping_dict.items()
        if v["casrec_table"].lower() == source_table_name
        and v["casrec_column_name"] != "unknown"
    ]
    columns = {k: v for d in simple_column_remap for k, v in d.items()}

    return source_data.rename(columns=columns)


def squash_columns(cols_to_squash, new_col, df, drop_original_cols=True):
    df[new_col] = df[cols_to_squash].values.tolist()
    df[new_col] = df[new_col].apply(lambda x: json.dumps(x))

    if drop_original_cols:
        df = df.drop(columns=cols_to_squash)

    return df


def convert_to_bool(original_col, new_col, df, drop_original_col=True):
    df[new_col] = df[original_col] == "1.0"
    if drop_original_col:
        df = df.drop(columns=original_col)
    return df


def unique_number(new_col, df, length=12):
    df[new_col] = df.apply(
        lambda x: random.randint(10 ** (length - 1), 10 ** length - 1), axis=1
    )

    return df


def date_format_standard(original_col, aggregate_col, df):
    df["new"] = df[original_col].astype(str)
    df["new"] = pd.to_datetime(df["new"], format="%Y-%m-%d %H:%M:%S")
    df["new"] = [x.strftime("%Y-%m-%d") for x in df.new]

    df = df.drop(columns=original_col)
    df = df.rename(columns={"new": aggregate_col})

    return df


def do_transformations(df, transformations):

    transformed_df = df
    if len(transformations) > 0:
        if "squash_columns" in transformations:
            for t in transformations["squash_columns"]:
                transformed_df = squash_columns(
                    t["original_columns"], t["aggregate_col"], transformed_df
                )
        if "convert_to_bool" in transformations:
            for t in transformations["convert_to_bool"]:
                transformed_df = convert_to_bool(
                    t["original_columns"], t["aggregate_col"], transformed_df
                )
        if "date_format_standard" in transformations:
            for t in transformations["date_format_standard"]:
                transformed_df = date_format_standard(
                    t["original_columns"], t["aggregate_col"], transformed_df
                )
        if "unique_number" in transformations:
            for t in transformations["unique_number"]:
                transformed_df = unique_number(t["aggregate_col"], transformed_df)
    else:
        transformed_df = df

    return transformed_df


def populate_required_columns(df, required_cols):
    for col, details in required_cols.items():
        df[col] = details["default_value"]

    return df


# Not really for here but got no where else sensible to put it at the moment
def get_next_sirius_id(engine, sirius_table_name):

    query = f"select max(id) from {sirius_table_name};"
    max_id = engine.execute(query).fetchall()
    next_id = max_id[0][0] + 1

    return next_id


def add_incremental_ids(df, column_name, starting_number):
    df.insert(0, column_name, range(starting_number, starting_number + len(df)))

    return df
