import logging
import os

import helpers
from helpers import get_mapping_dict, list_all_mapping_files


log = logging.getLogger("root")
environment = os.environ.get("ENVIRONMENT")


config = helpers.get_config(env=environment)


def get_lookups_to_sync():
    mapping_files = list_all_mapping_files()

    lookups_to_sync = {}
    for file in mapping_files:
        file_name = file[:-5]
        mapping_dict = get_mapping_dict(
            file_name=file_name, stage_name="migration-initialise-environments"
        )

        for field, details in mapping_dict.items():
            if "sync_lookup" in details["sync"]:
                lookup_def = get_mapping_dict(
                    file_name=file_name, stage_name="transform_casrec"
                )[field]["lookup_table"]
                sirius_table = get_mapping_dict(
                    file_name=file_name, stage_name="sirius_details"
                )[field]["table_name"]
                lookup_table = get_mapping_dict(
                    file_name=file_name, stage_name="sirius_details"
                )[field]["fk_parents"].split(":")[0]

                if sirius_table in lookups_to_sync:
                    lookups_to_sync[sirius_table].append(
                        {field: {lookup_def: lookup_table}}
                    )
                else:
                    lookups_to_sync[sirius_table] = [
                        {field: {lookup_def: lookup_table}}
                    ]

    return lookups_to_sync
