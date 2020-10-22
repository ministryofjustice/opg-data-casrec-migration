import json
import os


from mapping import Mapping

mapping_document = "docs/mapping_doc.xlsx"


tables = {
    "cases": {
        "sheet_name": "cases",
        "source_table_name": "order",
        "source_table_additional_columns": ["Order No"],
        "destination_table_name": "cases",
    }
}

for table in tables.keys():

    mapping_from_excel = Mapping(
        excel_doc=mapping_document, table_definitions=tables[table]
    )

    mapping_dict = mapping_from_excel.mapping_definitions()
    mapping_dict[
        "source_data_query"
    ] = mapping_from_excel.generate_select_string_from_mapping()

    json_path = os.path.join("tables", table)

    if not os.path.exists(json_path):
        os.makedirs(json_path)

    with open(f"{json_path}/mapping.json", "w") as json_out:
        json.dump(mapping_dict, json_out)
