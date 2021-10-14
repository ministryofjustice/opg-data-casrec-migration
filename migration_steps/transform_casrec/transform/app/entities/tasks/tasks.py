import logging

import pandas as pd
from utilities.basic_data_table import get_basic_data_table

from custom_errors import EmptyDataFrame
from helpers import get_mapping_dict, get_table_def

log = logging.getLogger("root")

def insert_tasks(db_config, target_db, mapping_file):
    chunk_size = db_config["chunk_size"]
    offset = -chunk_size
    chunk_no = 0

    mapping_file_name = f"{mapping_file}_mapping"
    table_definition = get_table_def(mapping_name=mapping_file)
    sirius_details = get_mapping_dict(
        file_name=mapping_file_name,
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    while True:
        offset += chunk_size
        chunk_no += 1

        try:
            # this throws EmptyDataFrame exception if there are no more records
            tasks_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            num_tasks = len(tasks_df)

            # filter so we only have ACTIVE and INACTIVE statuses
            tasks_df = tasks_df[tasks_df['status'].str.contains(r'ACTIVE|INACTIVE')]

            # only attempt the insert if we have tasks left to insert
            if num_tasks > 0:
                # set status to 'Not started'; note that we have to do this here,
                # as we need the original status as-is to filter out undesirable records
                tasks_df['status'] = 'Not started'

                target_db.insert_data(
                    table_name=table_definition["destination_table_name"],
                    df=tasks_df,
                    sirius_details=sirius_details,
                    chunk_no=chunk_no,
                )
            else:
                log.info(f'Chunk originally had {num_tasks} tasks, but was filtered to 0; ignoring')

        except EmptyDataFrame:
            log.info('Creating empty tasks table')
            target_db.create_empty_table(sirius_details=sirius_details)
            break

        except Exception as e:
            log.exception(e)
            break
