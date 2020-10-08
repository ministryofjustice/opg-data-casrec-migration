"""
create and insert the notes table
"""
from transformations.single_data_table import all_steps

definition = {
    "sheet_name": "notes",
    "source_table_name": "remarks",
    "sirius_table_name": "notes",
}


def final():
    final_df = all_steps(table_definition=definition)

    return final_df
