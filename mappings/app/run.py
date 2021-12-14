import json
import os
import shutil
from glob import glob
from config import config
from generate_all_files import generate_files


def remove_old_files():

    path = f"./{config['DEFINITION_PATH']}"

    try:
        shutil.rmtree(path)

    except Exception as e:
        print(f"e: {e}")


def loop_through_files():

    remove_old_files()

    destination = config["DEFINITION_PATH"]

    # As table defs is a single file which spans all spreadsheets, we gather
    # the definitions into a directory and write once into a file once we've read them all
    all_table_defs = {}

    for mapping_file_path in glob(os.path.join(config["SPREADSHEET_PATH"], "*.xlsx")):

        if os.path.isfile(mapping_file_path):
            if "~$" not in mapping_file_path:
                print(f"mapping_file: {mapping_file_path}")

                new_table_defs = generate_files(
                    spreadsheet_path=mapping_file_path,
                    destination=destination,
                )

                all_table_defs.update(new_table_defs)

    # write table defs to file
    path = f"./{destination}/tables"

    if not os.path.exists(path):
        os.makedirs(path)

    with open(f"{path}/table_definitions.json", "w") as table_defs_file:
        json.dump(all_table_defs, table_defs_file, indent=4, sort_keys=True)
