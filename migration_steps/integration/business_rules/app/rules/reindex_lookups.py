from helpers import get_mapping_dict, list_all_mapping_files

parent_table = "bonds"
parent_match_col = "bond_provider_id"
lookup_table = "bond_providers"
lookup_result_col = "id"
lookup_match_col = "uid"


def get_lookups_to_reindex():
    mapping_files = list_all_mapping_files()

    lookups_to_reindex = {}
    for file in mapping_files:
        file_name = file[:-5]
        mapping_dict = get_mapping_dict(file_name=file_name, stage_name="integration")
        for field, details in mapping_dict.items():
            if "reindex_lookup" in details["business_rules"]:
                transform_mapping_dict = get_mapping_dict(
                    file_name=file_name, stage_name="transform_casrec"
                )
                lookup_table = transform_mapping_dict[field]["lookup_table"]
                if file_name in lookups_to_reindex:
                    lookups_to_reindex[file_name].append({field: lookup_table})
                else:
                    lookups_to_reindex[file_name] = [{field: lookup_table}]

    # print(f"lookups_to_reindex: {lookups_to_reindex}")
    return lookups_to_reindex


def reindex_lookup():
    pass
