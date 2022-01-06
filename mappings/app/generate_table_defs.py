import os
import json
import numpy as np


def create_table_def_json(df, name):
    print(f"--- creating table defs: {name}")
    print(f"name: {name}")

    df = df.replace(np.nan, "")
    df = df.rename(columns={"casrec_conditions": "source_conditions"})
    df = df.set_index("mapping_file_name")

    try:
        df = df.drop(columns="Unnamed: 8")
    except Exception:
        pass
    table_def_dict = df.to_dict("index")

    convert_col_to_list(
        column_names=["source_table_additional_columns"], definition_dict=table_def_dict
    )
    convert_col_to_dict(
        column_names=["source_conditions", "table_transforms"],
        definition_dict=table_def_dict,
    )

    table_defs = {}
    for mapping_file_name, details in table_def_dict.items():
        table_defs[mapping_file_name] = details

    return table_defs


def convert_col_to_list(column_names, definition_dict):
    for col, details in definition_dict.items():
        for field in column_names:
            try:
                details[field] = [x.strip() for x in details[field].split(",")]
            except Exception:
                details[field] = [details[field]]

    return definition_dict


def convert_col_to_dict(column_names, definition_dict):
    for col, details in definition_dict.items():
        for field in column_names:
            try:
                conditions = [x for x in details[field].split("\n")]
                condition_details = {}
                for condition in conditions:
                    key = condition.split("=")[0].strip()
                    raw_val = condition.split("=")[1].strip()
                    try:
                        val = json.loads(raw_val)
                    except Exception:
                        val = raw_val

                    condition_details[key] = val
                details[field] = condition_details
            except KeyError as key:
                print(f"No key {key} in definition for table - ignoring")
                details[field] = {}
            except Exception as e:
                print(e)
                details[field] = {}
                pass
    return definition_dict
