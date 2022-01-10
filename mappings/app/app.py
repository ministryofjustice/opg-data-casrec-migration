import json
import os
import pandas as pd
import shutil
from glob import glob

from config import config
from generate_json_def import generate_json_files
from generate_lookup_table_json import create_lookup_table_json
from generate_table_defs import create_table_def_json


def _remove_old_files(dest_dir):
    try:
        shutil.rmtree(dest_dir)
    except Exception as e:
        print(f"e: {e}")


def _generate_files(spreadsheet_dir, dest_dir):
    print(f"spreadsheet: {spreadsheet_dir}")
    dirname = os.path.dirname(__file__)

    file_path = os.path.join(dirname, "..", spreadsheet_dir)
    excel_df = pd.ExcelFile(file_path)

    all_table_defs = {}
    for sheet in excel_df.sheet_names:
        print(f"sheet: {sheet}")
        df = pd.read_excel(excel_df, sheet_name=sheet)
        if "table_definition" in sheet:
            new_table_defs = create_table_def_json(df=df, name=sheet)
            all_table_defs.update(new_table_defs)
        elif "lookup" in sheet:
            create_lookup_table_json(df=df, name=sheet, destination=dest_dir)
        else:
            generate_json_files(df=df, name=sheet, destination=dest_dir)

    return all_table_defs


def _read_spreadsheets(spreadsheet_dir, dest_dir):
    # As table defs is a single file which spans all spreadsheets, we gather
    # the definitions into a directory and write once into a file once we've read them all
    all_table_defs = {}

    for mapping_file_path in glob(os.path.join(spreadsheet_dir, "*.xlsx")):
        if "~$" not in mapping_file_path:
            print(f"mapping_file: {mapping_file_path}")

            new_table_defs = _generate_files(
                spreadsheet_dir=mapping_file_path,
                dest_dir=dest_dir,
            )

            all_table_defs.update(new_table_defs)

    # write table defs to file
    path = f"./{dest_dir}/tables"

    if not os.path.exists(path):
        os.makedirs(path)

    with open(f"{path}/table_definitions.json", "w") as table_defs_file:
        json.dump(all_table_defs, table_defs_file, indent=4, sort_keys=True)


if __name__ == "__main__":
    dest_dir = f"./{config['DEFINITION_PATH']}"
    spreadsheet_dir = config["SPREADSHEET_PATH"]

    _remove_old_files(dest_dir)
    _read_spreadsheets(spreadsheet_dir, dest_dir)
