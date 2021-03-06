import random

import pandas as pd
import os
from faker import Faker
import time

start = time.time()

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

data_dir = "data"
anon_data_dir = "anon_data"
fake = Faker("en-GB")

try:
    os.remove("change_log.txt")
    os.mkdir("anon_data")
except OSError:
    pass

log_file = open(
    "change_log.txt",
    "a",
)

id = {
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

    include_cols = id[data_name]["include"]
    exclude_cols = id[data_name]["exclude"]

    if exact_match:
        matching_columns = [x for x in columns if x.lower() in include_cols]
        cols_to_change = [x for x in matching_columns if x not in exclude_cols]
    else:
        matching_columns = [
            x for x in columns if any(i in x.lower() for i in include_cols)
        ]
        cols_to_change = [x for x in matching_columns if x not in exclude_cols]

    return cols_to_change


for file in os.listdir(data_dir):
    file_name = file.split(".")[0]
    log_file.write(f"===== Starting file {file_name} ===== \n")
    file_start = time.time()
    columns_changed = []

    df = pd.read_csv(os.path.join(data_dir, file))

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
                    except:
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
            except:
                df.loc[index, documents] = fake.catch_phrase()
            if documents not in columns_changed:
                columns_changed.append(documents)

    column_list = [", ".join(x) for x in columns_changed]
    log_file.write(f"{', '.join(column_list)} \n")

    df.to_csv(os.path.join(anon_data_dir, file))

    log_file.write(
        f"===== Finished anonymising {len(df)} rows in {file_name} in"
        f" {round(time.time() - file_start, 2)} secs "
        f"===== \n\n\n"
    )

log_file.write(f"Total time: {time.time()-start}")
log_file.close()
print(f"Time: {time.time()-start}")
