import logging

import pandas as pd
from utilities.basic_data_table import get_basic_data_table
from utilities.standard_transformations import coalesce

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

    # only migrate tasks with a case no. which corresponds to one
    # in the cases table
    cases_df = pd.read_sql_query(
        f"SELECT DISTINCT caserecnumber FROM {db_config['target_schema']}.cases",
        db_config["db_connection_string"],
    )

    while True:
        offset += chunk_size
        chunk_no += 1

        try:
            # this raises EmptyDataFrame exception if there are no more records
            tasks_df = get_basic_data_table(
                db_config=db_config,
                mapping_file_name=mapping_file_name,
                table_definition=table_definition,
                sirius_details=sirius_details,
                chunk_details={"chunk_size": chunk_size, "offset": offset},
            )

            # inner join to cases to exclude tasks with a case no. not in that table
            tasks_df = tasks_df.merge(
                cases_df, how="inner", left_on="c_case", right_on="caserecnumber"
            )

            # duedate = Start Sate from simple mapping, unless casrec target is set,
            # in which case use that
            tasks_df = coalesce(["c_target", "duedate"], "duedate", tasks_df)

            num_tasks = len(tasks_df)

            # check before insert, otherwise an empty dataframe causes EmptyDataFrame
            # exception, which would lead to skipping later chunks
            if len(tasks_df) > 0:
                target_db.insert_data(
                    table_name=table_definition["destination_table_name"],
                    df=tasks_df,
                    sirius_details=sirius_details,
                    chunk_no=chunk_no,
                )
            else:
                log.info(
                    f"Chunk originally had {num_tasks} tasks, but was filtered to 0; ignoring"
                )

        except EmptyDataFrame as empty_data_frame:
            if empty_data_frame.empty_data_frame_type == "chunk":
                target_db.create_empty_table(
                    sirius_details=sirius_details, df=empty_data_frame.df
                )
                break
            continue
