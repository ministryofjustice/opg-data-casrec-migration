"""
create and insert the persons table
"""
import time

from transformations.single_data_table import all_steps


definition = {
    "sheet_name": "persons (Deputy)",
    "source_table_name": "deputy",
    "sirius_table_name": "persons",
}


def final():

    final_df = all_steps(table_definition=definition)

    return final_df
