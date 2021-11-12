import os
import sys
import json
import shutil
import pandas as pd
from pathlib import Path
from faker import Faker
from dotenv import load_dotenv

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../migration_steps/shared")
pd.options.mode.chained_assignment = None

# Initialise variables
mapping_file_path = (
    str(current_path) + "/../../migration_steps/shared/mapping_definitions"
)
backup_file_path = str(current_path) + "/../../data/anon_data_backup"
anon_data_file_path = str(current_path) + "/../../data/anon_data"
data_path = f"{current_path}/../../data/anon_data/"
current_path = Path(os.path.dirname(os.path.realpath(__file__)))
env_path = current_path / "../../migration_steps/.env"
load_dotenv(dotenv_path=env_path)
environment = os.environ.get("ENVIRONMENT")
fake = Faker("en-GB")

anon_types = {
    "first_name": {
        "include": ["forename", "firstname", "aka"],
        "exclude": [],
        "faker": "first_name_nonbinary",
    },
    "surname": {
        "include": ["surname", "lastname", "last_name"],
        "exclude": [],
        "faker": "last_name_nonbinary",
    },
    "full_name": {"include": ["name"], "exclude": [], "faker": "name"},
    "title": {"include": ["title"], "exclude": [], "faker": "prefix_nonbinary"},
    "initial": {
        "include": ["init"],
        "exclude": ["rev_init"],
    },
    "dob": {"include": ["dob"], "exclude": [], "faker": "date"},
    "birth_year": {
        "include": ["birth_yr"],
        "exclude": [],
    },
    "date": {"include": ["date", "sent1"], "exclude": [], "faker": "datetime"},
    "email": {"include": ["email"], "exclude": ["by_email"], "faker": "email"},
    "phone": {
        "include": ["phone", "mobile", "tele"],
        "exclude": ["papers_to_phone", "papers to phone", "assrc_tele_comp"],
        "faker": "phone_number",
    },
    "address1": {"include": ["adrs1"], "exclude": [], "faker": "street_address"},
    "address": {"include": ["adrs"], "exclude": ["adrs1"], "faker": "city"},
    "postcode": {"include": ["postcode"], "exclude": [], "faker": "postcode"},
    "solicitor_name": {
        "include": ["sender_co", "sender co", "pathfinder"],
        "exclude": [],
        "faker": "company",
    },
    "invoice_number": {"include": ["invoice no"], "exclude": [], "faker": "invoice_no"},
}

edge_cases = [
    {
        "description": "percentage in text fields",
        "replacement_data": "%",
        "override": False,
        "data_type": "str",
    },
    {
        "description": "apostrophe in text fields",
        "replacement_data": "'",
        "override": False,
        "data_type": "str",
    },
    {
        "description": "speech mark in text fields",
        "replacement_data": '"',
        "override": False,
        "data_type": "str",
    },
    {
        "description": "ampersand in text fields",
        "replacement_data": "&",
        "override": False,
        "data_type": "str",
    },
    {
        "description": "null text fields",
        "replacement_data": "",
        "override": True,
        "data_type": "str",
    },
    {
        "description": "null in int fields",
        "replacement_data": "",
        "override": True,
        "data_type": "int",
    },
    {
        "description": "float in int fields",
        "replacement_data": "2.0",
        "override": True,
        "data_type": "int",
    },
    {
        "description": "date in datetime fields",
        "replacement_data": "2021-01-01",
        "override": True,
        "data_type": "datetime",
    },
    {
        "description": "datetime in date fields",
        "replacement_data": "2021-01-01",
        "override": True,
        "data_type": "date",
    },
    {
        "description": "YY year format",
        "replacement_data": "21-01-01",
        "override": True,
        "data_type": "datetime",
    },
    {
        "description": "null in date fields",
        "replacement_data": "",
        "override": True,
        "data_type": "date",
    },
    {
        "description": "null in datetime fields",
        "replacement_data": "",
        "override": True,
        "data_type": "datetime",
    },
]


def get_anon_type(column):
    for anon_type in anon_types:
        matching_column = (
            column
            if any(i in column.lower() for i in anon_types[anon_type]["include"])
            else None
        )
        actual_match = (
            column
            if column.lower() in anon_types[anon_type]["exclude"]
            else matching_column
        )
        if actual_match is not None:
            return anon_types[anon_type]["faker"]
    return "original_value"


def update_casrec_fields(table, column, data_type, fields):
    field = {
        "table": str(table).lower(),
        "column": column,
        "data_type": data_type,
        "anon_type": get_anon_type(column),
    }

    if column not in ["Case", "Order No", "Deputy No"]:
        fields.append(field)

    return fields


def backup_anon_data():
    for file_name in os.listdir(anon_data_file_path):
        source = f"{anon_data_file_path}/{file_name}"
        destination = f"{backup_file_path}/{file_name}"
        shutil.copy(source, destination)


def get_max_case_reference():
    df = pd.read_csv(data_path + "pat.csv")
    return df["Case"].max()


def get_max_order_no():
    df = pd.read_csv(data_path + "order.csv")
    return df["Order No"].max()


def get_max_deputy_no():
    df = pd.read_csv(data_path + "deputy.csv")
    return df["Deputy No"].max()


def get_max_rct_no(df):
    return df["rct"].max()


def get_field_value(field_info_obj, current_col_value):
    anon_type = field_info_obj["anon_type"]

    if anon_type == "first_name_nonbinary":
        column_value = fake.first_name_nonbinary()
    elif anon_type == "last_name_nonbinary":
        column_value = fake.last_name_nonbinary()
    elif anon_type == "name":
        column_value = fake.name()
    elif anon_type == "prefix_nonbinary":
        column_value = fake.prefix_nonbinary()
    elif anon_type == "date":
        column_value = fake.date(pattern="%Y-%m-%d")
    elif anon_type == "datetime":
        column_value = fake.date(pattern="%Y-%m-%d %H:%M:%S")
    elif anon_type == "email":
        column_value = fake.email()
    elif anon_type == "phone_number":
        column_value = fake.phone_number()[:10]
    elif anon_type == "street_address":
        column_value = fake.street_address().replace("\n", "")
    elif anon_type == "city":
        column_value = fake.city()
    elif anon_type == "postcode":
        column_value = fake.postcode()
    elif anon_type == "company":
        column_value = fake.company()
    elif anon_type == "invoice_no":
        column_value = fake.bothify(text="S3#####/##")
    else:
        column_value = current_col_value

    return column_value


def get_final_replacement_value(replace_value, edge_case_object):
    ignore_values = ["nan", "NaT", "<NA>"]
    if replace_value in ignore_values:
        value = replace_value
    elif edge_case_object["override"] and replace_value not in ignore_values:
        value = edge_case_object["replacement_data"]
    else:
        value = f'{replace_value}{edge_case_object["replacement_data"]}'

    return value


def in_ignore_list(col):
    ignore_list = [
        "Marital Status",
        "c_amount",
        "Amount",
        "Date Create",
        "Log Date",
        "Logdate",
        "Score",
        "End Date",
        "Bond Co",
    ]
    if col in ignore_list:
        return True
    else:
        return False


def empty_output_directory(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


def get_mappings_objects():
    casrec_tables = []
    casrec_fields = []
    for json_file in os.listdir(mapping_file_path):
        json_file_path = os.path.join(mapping_file_path, json_file)
        if os.path.isfile(json_file_path):
            with open(json_file_path, "r") as definition_json:
                def_dict = json.load(definition_json)
                for field, details in def_dict.items():
                    if details["transform_casrec"]["casrec_column_name"] != "":

                        if isinstance(
                            details["transform_casrec"]["casrec_column_name"], list
                        ):
                            for col in details["transform_casrec"][
                                "casrec_column_name"
                            ]:
                                casrec_fields = update_casrec_fields(
                                    details["transform_casrec"]["casrec_table"],
                                    col,
                                    details["sirius_details"]["data_type"],
                                    casrec_fields,
                                )
                        else:
                            casrec_fields = update_casrec_fields(
                                details["transform_casrec"]["casrec_table"],
                                details["transform_casrec"]["casrec_column_name"],
                                details["sirius_details"]["data_type"],
                                casrec_fields,
                            )

                        casrec_tables.append(
                            str(details["transform_casrec"]["casrec_table"]).lower()
                        )
    unique_tables = sorted(set(casrec_tables))

    return unique_tables, casrec_fields


def reformat_mappings_object(unique_tables, casrec_fields):
    all_tables = {}
    for table in unique_tables:
        table_fields = []
        for field in casrec_fields:
            if field["table"] == table:
                field_info = {
                    "column": field["column"],
                    "data_type": str(field["data_type"]).replace("dict", "str"),
                    "anon_type": field["anon_type"],
                }
                table_fields.append(field_info)

        all_tables[table] = table_fields

    for table in all_tables:
        print(table)
        for col in all_tables[table]:
            print(col)

    return all_tables


def get_initial_table_rows(unique_tables):
    initial_table_rows = {}
    for table_name in unique_tables:
        print(f"Replacing fields in table: {table_name}")
        file_path = data_path + table_name + ".csv"
        print("Reading the CSV")
        df = pd.read_csv(file_path)
        print("Getting last col")
        df_single_row = df.iloc[[-1]]
        df_single_row = df_single_row.copy()
        initial_table_rows[table_name] = df_single_row
        file = open(f"{anon_data_file_path}/{table_name}.csv", "a")
        file.write("\n")
        file.close()

    return initial_table_rows


def update_row_key(df_single_row, df_single_row_modified, seed_modifier):
    try:
        record_id = get_max_rct_no(df_single_row) + seed_modifier
        df_single_row_modified["rct"] = record_id
        df_single_row_modified.iloc[0, 0] = record_id
    except Exception as e:
        pass

    return df_single_row_modified


def update_row_primary_keys(df_single_row_modified, primary_keys):
    for primary_key in primary_keys:
        try:
            # print(f'Replacing {primary_key["column"]}')
            if primary_key["column"] in df_single_row_modified:
                df_single_row_modified[primary_key["column"]] = primary_key["id"]
        except Exception as e:
            pass

    return df_single_row_modified


def update_row_fields(field_info, df_single_row, edge_case):
    initial_replacement_value = str(
        get_field_value(field_info, df_single_row[field_info["column"]].values[0])
    )

    if field_info["data_type"] == edge_case["data_type"] and not in_ignore_list(
        field_info["column"]
    ):
        final_replacement_value = get_final_replacement_value(
            initial_replacement_value, edge_case
        )
    else:
        final_replacement_value = initial_replacement_value

    print(f'Replacing {field_info["column"]}')

    return final_replacement_value


def main():
    backup_anon_data()
    unique_tables, casrec_fields = get_mappings_objects()
    print(unique_tables)
    all_tables = reformat_mappings_object(unique_tables, casrec_fields)
    initial_seed_caserec_number = 99990001
    initial_seed_order_number = get_max_order_no()
    initial_seed_deputy_number = get_max_deputy_no()

    empty_output_directory(output_path)

    initial_table_rows = get_initial_table_rows(unique_tables)

    seed_modifier = 0
    for edge_case in edge_cases:
        print("Creating edge case: " + edge_case["description"])
        seed_modifier += 1

        primary_keys = [
            {"column": "Case", "id": initial_seed_caserec_number + seed_modifier},
            {
                "column": "CoP Case",
                "id": f"{str(initial_seed_caserec_number + seed_modifier)}01",
            },
            {"column": "Order No", "id": initial_seed_order_number + seed_modifier},
            {"column": "Deputy No", "id": initial_seed_deputy_number + seed_modifier},
        ]

        for table_row in initial_table_rows:
            print(f"Starting replacements on table: {table_row}")
            df_single_row = initial_table_rows[table_row].copy()
            df_single_row_modified = df_single_row.copy()
            df_single_row_modified = update_row_key(
                df_single_row, df_single_row_modified.copy(), seed_modifier
            )
            df_single_row_modified = update_row_primary_keys(
                df_single_row_modified.copy(), primary_keys
            )

            for field_info in all_tables[table_row]:
                final_replacement_value = update_row_fields(
                    field_info, df_single_row, edge_case
                )
                if field_info["column"] in df_single_row_modified:
                    df_single_row_modified[
                        field_info["column"]
                    ] = final_replacement_value

            df_single_row_modified.to_csv(
                f"{anon_data_file_path}/{table_row}.csv",
                mode="a",
                index=False,
                header=False,
            )


if __name__ == "__main__":
    main()
