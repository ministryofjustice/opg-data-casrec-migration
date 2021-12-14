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

    for mapping_file_path in glob(os.path.join(config["SPREADSHEET_PATH"], "*.xlsx")):

        if os.path.isfile(mapping_file_path):
            if "~$" not in mapping_file_path:
                print(f"mapping_file: {mapping_file_path}")
                generate_files(
                    spreadsheet_path=mapping_file_path,
                    destination=config["DEFINITION_PATH"],
                )
