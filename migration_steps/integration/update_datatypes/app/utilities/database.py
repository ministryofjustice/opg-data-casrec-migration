from typing import Dict


def generate_select_string(mapping_details: Dict, schema: str, table_name: str) -> str:
    cols = ", ".join(list(mapping_details.keys()))
    statement = f"SELECT {cols} from {schema}.{table_name};"

    return statement


def generate_create_statement(
    mapping_details: Dict, schema: str, table_name: str
) -> str:

    statement = f"CREATE TABLE {schema}.{table_name} (\n"

    columns = []
    for col, details in mapping_details.items():
        columns.append(f"{col} {details['data_type']}")
        if details["is_pk"] is True or details["fk_parents"] is not None:
            columns.append(f"sirius_{col} {details['data_type']}")

    statement += ", ".join(columns)

    statement += ");"

    return statement


def generate_mapping_table_create(
    mapping_details: Dict, schema: str, table_name: str, entity_name: str
) -> str:

    statement = f"CREATE TABLE {schema}.sirius_map_{entity_name}_{table_name} (\n"

    columns = []
    for col, details in mapping_details.items():
        if col in ["caserecnumber"]:
            columns.append(f"{col} {details['data_type']}")
        if details["is_pk"] is True or len(details["fk_parents"]) > 0:
            columns.append(f"sirius_{col} {details['data_type']}")

    statement += ", ".join(columns)

    statement += ");"

    return statement


def insert_data():
    pass
