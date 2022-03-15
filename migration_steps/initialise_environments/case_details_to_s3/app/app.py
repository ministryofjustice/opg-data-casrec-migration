import sys
import os
import random
from pathlib import Path

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../shared")

import time
from helpers import get_config
from dotenv import load_dotenv
import helpers
from db_helpers import *
from helpers import *
import logging
import custom_logger
import click
from sqlalchemy import create_engine
import pandas as pd
import pprint
import boto3
from faker import Faker

pp = pprint.PrettyPrinter(indent=4)

env_path = current_path / "../../../../.env"
shared_path = current_path / "../../../shared"
temp_csv_path = shared_path / "temp/csvs"
load_dotenv(dotenv_path=env_path)

environment = os.environ.get("ENVIRONMENT")
config = get_config(environment)

# logging
log = logging.getLogger("root")
log.addHandler(custom_logger.MyHandler())
config.custom_log_level()
verbosity_levels = config.verbosity_levels

engine = None
target_schema = None
source_schema = config.schemas["pre_transform"]
mapping_dict = None

s3_url = os.environ.get("S3_URL")

ci = os.getenv("CI")
account_name = os.environ.get("ACCOUNT_NAME")
bucket_name = f"casrec-migration-{account_name.lower()}"
account = os.environ["SIRIUS_ACCOUNT"]


def get_anon_id():
    return {
        "first_name": {
            "include": ["forename", "firstname", "aka"],
            "exclude": [],
        },
        "surname": {
            "include": ["surname", "lastname", "last_name"],
            "exclude": [],
        },
        "full_name": {
            "include": ["name"],
            "exclude": [],
        },
        "title": {
            "include": ["title"],
            "exclude": [],
        },
        "initial": {
            "include": ["init"],
            "exclude": ["Rev_Init"],
        },
        "dob": {
            "include": ["dob"],
            "exclude": [],
        },
        "birth_year": {
            "include": ["birth_yr"],
            "exclude": [],
        },
        "email": {
            "include": ["email"],
            "exclude": ["by_Email"],
        },
        "phone": {
            "include": ["phone", "mobile", "tele"],
            "exclude": ["Papers_to_Phone", "Papers to Phone", "Assrc_Tele_Comp"],
        },
        "address": {
            "include": ["adrs"],
            "exclude": [],
        },
        "postcode": {
            "include": ["postcode"],
            "exclude": [],
        },
        "free_text": {
            "include": ["comment", "note", "remarks", "sup_desc", "sup desc"],
            "exclude": [],
        },
        "documents": {
            "include": ["docid"],
            "exclude": [],
        },
        "payslip": {"include": ["payslip"], "exclude": []},
        "solicitor_name": {
            "include": ["sender_co", "sender co", "pathfinder", "pathfinder"],
            "exclude": [],
        },
    }


def get_cols(data_name, columns, exact_match=False):

    include_cols = get_anon_id()[data_name]["include"]
    exclude_cols = get_anon_id()[data_name]["exclude"]

    if exact_match:
        matching_columns = [x for x in columns if x.lower() in include_cols]
        cols_to_change = [x for x in matching_columns if x not in exclude_cols]
    else:
        matching_columns = [
            x for x in columns if any(i in x.lower() for i in include_cols)
        ]
        cols_to_change = [x for x in matching_columns if x not in exclude_cols]

    return cols_to_change


def anonymise_data(data):
    fake = Faker("en-GB")
    file_start = time.time()
    columns_changed = []

    df = data

    # Names
    titles = get_cols("title", df.columns)
    first_names = get_cols("first_name", df.columns)
    initials = get_cols("initial", df.columns)
    surnames = get_cols("surname", df.columns)
    full_names = get_cols("full_name", df.columns, exact_match=True)

    # dob
    dobs = get_cols("dob", df.columns)
    birth_years = get_cols("birth_year", df.columns)

    # email
    emails = get_cols("email", df.columns)

    # phone
    phones = get_cols("phone", df.columns)

    # address
    addresses = get_cols("address", df.columns)
    postcodes = get_cols("postcode", df.columns)

    # free text
    free_text_fields = get_cols("free_text", df.columns)

    # documents
    documents = get_cols("documents", df.columns)

    # payslip
    payslips = get_cols("payslip", df.columns)

    # solicitor
    solicitor_names = get_cols("solicitor_name", df.columns)

    for index in df.index:

        replacements = [
            {
                "col_list": titles,
                "fake_data": fake.prefix_nonbinary(),
            },
            {
                "col_list": first_names,
                "fake_data": fake.first_name_nonbinary(),
            },
            {
                "col_list": surnames,
                "fake_data": fake.last_name_nonbinary(),
            },
            {
                "col_list": full_names,
                "fake_data": fake.name(),
            },
            {
                "col_list": dobs,
                "fake_data": fake.date(pattern="%Y-%m-%d %H:%M:%S"),
            },
            {
                "col_list": emails,
                "fake_data": fake.email(),
            },
            {
                "col_list": phones,
                "fake_data": fake.phone_number(),
            },
            {
                "col_list": postcodes,
                "fake_data": fake.postcode(),
            },
            {
                "col_list": free_text_fields,
                "fake_data": fake.catch_phrase(),
            },
            {
                "col_list": solicitor_names,
                "fake_data": f"{fake.company()} {fake.company_suffix()}",
            },
            {
                "col_list": payslips,
                "fake_data": random.randint(100000, 1000000),
            },
        ]

        # simple replacements
        for r in replacements:
            if len(r["col_list"]) > 0:
                for i, col in enumerate(r["col_list"], start=1):
                    df.loc[index, col] = r["fake_data"]

                if r["col_list"] not in columns_changed:
                    columns_changed.append(r["col_list"])

        # complicated replacements
        if len(addresses) > 0:
            fake_address = fake.address()
            if len(addresses) > 1:
                for i, line in enumerate(addresses, start=0):
                    try:
                        df.loc[index, line] = fake_address.split("\n")[i]
                    except Exception:
                        df.loc[index, line] = ""

                if addresses not in columns_changed:
                    columns_changed.append(addresses)
            else:
                df.loc[index, addresses] = fake_address
                if addresses not in columns_changed:
                    columns_changed.append(addresses)

        # replacements that rely on other column data
        if len(initials) > 0 and len(first_names) > 0:
            df.loc[index, initials] = df.loc[index, first_names][0][0]
            if initials not in columns_changed:
                columns_changed.append(initials)

        if len(birth_years) > 0 and len(dobs) > 0:
            df.loc[index, birth_years] = df.loc[index, dobs][0][:4]
            if birth_years not in columns_changed:
                columns_changed.append(birth_years)

        if len(documents) > 0:
            try:
                rec_date = [
                    x for x in df.columns if x.lower() in ["date_rcvd", "date rcvd"]
                ]
                df.loc[index, documents] = (
                    f"{random.randint(100000, 1000000)}  "
                    f"{df.loc[index, rec_date][0]} "
                    f"{df.loc[index, 'Case']} "
                    f"{df.loc[index, surnames][0]}"
                )
            except Exception:
                df.loc[index, documents] = fake.catch_phrase()
            if documents not in columns_changed:
                columns_changed.append(documents)

    column_list = [", ".join(x) for x in columns_changed]
    log.info(f"Columns anonymised: {', '.join(column_list)}")

    log.info(
        f"===== Finished anonymising {len(df)} rows in"
        f" {round(time.time() - file_start, 2)} secs "
        f"===== \n\n"
    )

    df.fillna("")

    return df


def set_logging_level(verbose):
    try:
        log.setLevel(verbosity_levels[verbose])
    except KeyError:
        log.setLevel("INFO")
        log.info(f"{verbose} is not a valid verbosity level")


def get_primary_keys(case_ref):
    sql = f"""
    SELECT DISTINCT
    p."Case" as case,
    o."Order No"::numeric::integer as order_no,
    d."Deputy No"::numeric::integer as deputy_no,
    ds."Dep Addr No"::numeric::integer as dep_addr_no,
    ds."CoP Case" as cop_case
    FROM {config.schemas["pre_transform"]}.pat as p
    LEFT JOIN {config.schemas["pre_transform"]}.order as o ON p."Case" = o."Case"
    LEFT JOIN {config.schemas["pre_transform"]}.remarks r ON p."Case" = r."Case"
    LEFT JOIN {config.schemas["pre_transform"]}.deputyship  as ds ON o."Order No" = ds."Order No"
    LEFT JOIN {config.schemas["pre_transform"]}.deputy as d ON ds."Deputy No"::numeric::integer = d."Deputy No"::numeric::integer
    LEFT JOIN {config.schemas["pre_transform"]}.deputy_address as da ON da."Dep Addr No"::numeric::integer = ds."Dep Addr No"::numeric::integer
    WHERE p."Case" = '{case_ref}'
    """

    results = pd.read_sql_query(sql, engine)

    return results


def lower_snake(string):
    formatted_string = string.lower().replace(" ", "_")
    return formatted_string


def get_list_of_tables(pks, tables):
    list_of_tables = []
    log.info("in here...")
    log.info(pks)
    for table_pair in tables:
        log.info(table_pair)
        column_fmt = lower_snake(table_pair["pk"])
        log.info(pks[column_fmt])
        pks_fmt = "', '".join(
            list(
                set(
                    pks[column_fmt]
                    .dropna()
                    .astype(int, errors="ignore")
                    .astype(str)
                    .tolist()
                )
            )
        )
        sql = f"""
        SELECT *
        FROM {config.schemas["pre_transform"]}.{table_pair['table']}
        WHERE "{table_pair['pk']}" in ('{pks_fmt}')
        """
        log.info(sql)
        results = pd.read_sql_query(sql, engine)
        results.drop(
            columns=["casrec_row_id", "csv_record"], inplace=True, errors="ignore"
        )

        result_pair = {"table_name": table_pair["table"], "table_results": results}

        list_of_tables.append(result_pair)

    return list_of_tables


def set_connection_target():
    global engine
    db_config = "migration"
    db_conn_string = config.get_db_connection_string(db_config)
    engine = create_engine(db_conn_string)


def upload_csvs_to_s3():
    s3 = get_s3_session(environment, s3_url)
    if ci != "true":
        for file in os.listdir(temp_csv_path):
            if file.endswith(".csv"):
                file_path = f"{temp_csv_path}/{file}"
                s3_file_path = f"edge_cases_csvs/{file}"
                upload_file(bucket_name, file_path, s3, log, s3_file_path)


@click.command()
@click.option("-v", "--verbose", count=True)
@click.option("-c", "--caserecnumber", default="10000037")
def main(verbose, caserecnumber):
    set_logging_level(verbose)
    log.info(helpers.log_title(message="Extract and Anonymise Case"))

    set_connection_target()

    table_names = [
        {"table": "pat", "pk": "Case"},
        {"table": "order", "pk": "Order No"},
        {"table": "deputyship", "pk": "Order No"},
        {"table": "deputy", "pk": "Deputy No"},
        {"table": "remarks", "pk": "Case"},
        {"table": "deputy_address", "pk": "Dep Addr No"},
    ]
    log.info("=== GETTING DATA FOR CSVs (SQL below) ===")
    tables = get_list_of_tables(get_primary_keys(caserecnumber), table_names)

    log.info("=== ANONYMISING DATA ===")
    for table in tables:
        log.info(f"= {table['table_name']} =")
        table_name = table["table_name"]
        table["table_results"].to_csv(f"/shared/{table_name}.csv")
        anon_table = anonymise_data(table["table_results"])
        anon_table.to_csv(f"{temp_csv_path}/{table_name}_anon.csv")
    log.info("=== UPLOADING TO S3 ===")
    upload_csvs_to_s3()


if __name__ == "__main__":
    t = time.process_time()

    log.setLevel(1)
    log.debug(f"Working in environment: {os.environ.get('ENVIRONMENT')}")

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
