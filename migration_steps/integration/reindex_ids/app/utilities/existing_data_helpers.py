def get_tables_to_match(table_details):
    return {k: v for k, v in table_details.items() if "existing_data" in v}


def format_conditions(conditions):
    conditions_list = []

    for condition in conditions:
        if condition["condition_type"] == "equal":
            conditions_list.append(f"{condition['field']} = '{condition['value']}'")

    result = ""
    for i, condition in enumerate(conditions_list):
        if i == 0:
            result += f" WHERE {condition}"
        else:
            result += f" AND {condition}"

    return result
