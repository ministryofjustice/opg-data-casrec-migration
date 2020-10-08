


"""
create and insert the persons table
"""
from transformations.single_data_table import all_steps



definition = {
    "sheet_name": "persons (Client)",
    "source_table_name": "pat",
    "sirius_table_name": "persons",
}

def final():
    final_df = all_steps(table_definition=definition)

    return final_df



