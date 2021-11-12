import pandas as pd

from helpers import get_mapping_dict, get_table_def


def insert_person_task(db_config, target_db, mapping_file):
    sirius_details = get_mapping_dict(
        file_name=f"{mapping_file}_mapping",
        stage_name="sirius_details",
        only_complete_fields=False,
    )

    persons_query = (
        f"select id as person_id, caserecnumber from {db_config['target_schema']}.persons "
        f"where type = 'actor_client';"
    )
    persons_df = pd.read_sql_query(persons_query, db_config["db_connection_string"])

    tasks_query = (
        f'select id as task_id, c_case from {db_config["target_schema"]}.tasks;'
    )
    tasks_df = pd.read_sql_query(tasks_query, db_config["db_connection_string"])

    person_task_df = tasks_df.merge(
        persons_df,
        how="left",
        left_on="c_case",
        right_on="caserecnumber",
    )

    person_task_df = person_task_df[["person_id", "task_id"]]
    person_task_df["casrec_details"] = "{}"

    table_definition = get_table_def(mapping_name=mapping_file)
    target_db.insert_data(
        table_name=table_definition["destination_table_name"],
        df=person_task_df,
        sirius_details=sirius_details,
    )
