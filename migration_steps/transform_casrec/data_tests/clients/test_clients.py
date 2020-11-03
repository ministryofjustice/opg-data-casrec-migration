import json
import pandas as pd

from utilities.json_helpers import get_mapping_file


def test_clients(get_config):
    config = get_config
    sample_percentage = 1

    with open(get_mapping_file(file_name="persons_client_mapping")) as mapping_json:
        mapping_dict = json.load(mapping_json)

    destination_table = "persons"
    # destination_where = {"type": "actor_client"}

    destination_select_statement = (
        f"SELECT "
        f"{', '.join(k for k in mapping_dict.keys() if k != 'dob')} "
        f"from {config.etl2_schema}.{destination_table}"
        f";"
    )

    destination_df = pd.read_sql_query(
        destination_select_statement, config.connection_string
    )

    destination_sample_df = destination_df.sample(
        frac=sample_percentage / 100, replace=False, random_state=1
    )
    print(destination_sample_df.to_markdown())
