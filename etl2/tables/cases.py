


"""
create and insert the cases table
"""
from transformations.single_data_table import all_steps

definition = {
    "sheet_name": "cases",
    "source_table_name": "order",
    "sirius_table_name": "cases",
}

def final():
    final_df = all_steps(table_definition=definition)

    return final_df



