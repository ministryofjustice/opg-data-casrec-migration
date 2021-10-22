import pandas as pd


def get_person_task_records(db_config, mapping_file_name, table_definition, sirius_details, chunk_size, offset, prep):
    persons_query = (
        f"select id as person_id, caserecnumber from {db_config['target_schema']}.persons "
        f"where type = 'actor_client';"
    )
    persons_df = pd.read_sql_query(persons_query, db_config["db_connection_string"])

    tasks_query = f'select id as task_id, c_case from {db_config["target_schema"]}.tasks;'
    tasks_df = pd.read_sql_query(tasks_query, db_config["db_connection_string"])

    person_task_df = tasks_df.merge(
        persons_df,
        how="left",
        left_on="c_case",
        right_on="caserecnumber",
    )

    person_task_df = person_task_df[['person_id', 'task_id']]
    person_task_df["casrec_details"] = "{}"

    return (person_task_df, False)
