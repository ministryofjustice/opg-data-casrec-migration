# import json
# import os
#
#
# def get_mapping_dict(file_name: str) -> str:
#     dirname = os.path.dirname(__file__)
#     file_path = os.path.join(dirname, f"../mapping_definitions/{file_name}.json")
#
#     with open(file_path) as mapping_json:
#         mapping_dict = json.load(mapping_json)
#
#     return {k: v["transform_casrec"] for k, v in mapping_dict.items()}
#
#
# def get_lookup_dict(file_name: str) -> str:
#     dirname = os.path.dirname(__file__)
#     file_path = os.path.join(
#         dirname, f"../mapping_definitions/lookups" f"/{file_name}.json"
#     )
#
#     with open(file_path) as lookup_json:
#         lookup_dict = json.load(lookup_json)
#
#         return {k: v["sirius_mapping"] for k, v in lookup_dict.items()}
