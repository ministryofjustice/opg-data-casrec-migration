import pandas as pd
import os
from faker import Faker
import time
start = time.time()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

data_dir = 'data'
anon_data_dir = 'anon_data'
fake = Faker('en-GB')




id = {
    "first_name": ['forename', 'firstname', 'aka'],
    "surname": ['surname', 'lastname', 'last_name'],
    "title": ['title'],
    "initial": ['init'],
    "full_name": ['name'],
    "dob": ['dob'],
    "birth_year": ['birth_yr'],
    "email": ['email'],
    "phone": ['phone', 'mobile', 'contact_tele', 'day_tele'],
    "address": ['adrs'],
    "postcode": ['postcode'],
    "free_text": ['comment', 'note', 'remarks'],

}

def get_cols(data_name, columns):
    return [x for x in columns if any(i in x.lower() for i in id[data_name])]



for file in os.listdir(data_dir):
    file_name = file.split('.')[0]

    df = pd.read_csv(os.path.join(data_dir, file))

    # Names
    titles = get_cols('title', df.columns)
    first_names = get_cols('first_name', df.columns)
    initials = get_cols('initial', df.columns)
    surnames = get_cols('surname', df.columns)
    full_names = get_cols('full_name', df.columns)

    # dob
    dobs = get_cols('dob', df.columns)
    birth_years = get_cols('birth_year', df.columns)

    # email
    emails = get_cols('email', df.columns)

    # phone
    phones = get_cols('phone', df.columns)

    # address
    addresses = get_cols('address', df.columns)
    postcodes = get_cols('postcode', df.columns)

    # free text
    free_text_fields = get_cols('free_text', df.columns)




    for index in df.index:

        if len(titles) > 0:
            fake_title = fake.prefix_nonbinary()
            df.loc[index, titles] = fake_title

        if len(first_names) > 0:
            fake_name = fake.first_name_nonbinary()
            df.loc[index, first_names] = fake_name
            df.loc[index, initials] = fake_name[0]

        if len(surnames) > 0:
            fake_surname = fake.last_name_nonbinary()
            df.loc[index, surnames] = fake_surname

        if len(full_names) > 0:
            fake_full_name = fake.name_nonbinary()
            df.loc[index, full_names] = fake_full_name


        # dob
        if len(dobs) > 0:
            fake_dob = fake.date(pattern="%Y%m%d")
            fake_birth_year = fake_dob[:4]
            df.loc[index, dobs] = fake_dob
            df.loc[index, birth_years] = fake_birth_year

        # email
        if len(emails)> 0:
            for i, email in enumerate(emails, start=1):
                fake_email = fake.email()
                df.loc[index, email] = fake_email

        # phone
        if len(phones) > 0:
            for i, phone in enumerate(phones, start=1):
                fake_phone = fake.phone_number()
                df.loc[index, phone] = fake_phone


        # address
        if len(postcodes) > 0:
            fake_postcode = fake.postcode()
            df.loc[index, postcodes] = fake_postcode

        if len(addresses) > 0:
            fake_address = fake.address()
            if len(addresses) > 1:
                for i, line in enumerate(addresses, start=0):
                    try:
                        df.loc[index, line] = fake_address.split('\n')[i]
                    except:
                        df.loc[index, line] = ""
            else:
                df.loc[index, addresses] = fake_address


        # free text
        if len(free_text_fields)> 0:
            for i, comment in enumerate(free_text_fields, start=1):
                fake_comment = fake.catch_phrase()
                df.loc[index, comment] = fake_comment


    df.to_csv(os.path.join(anon_data_dir, file))




print(f"Time: {time.time()-start}")
