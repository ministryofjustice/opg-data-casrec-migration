import json
import random
import uuid

import pandas as pd
import psycopg2
from beeprint import pp

excel_doc = 'mapping_doc.xlsx'
# sheet_name = "persons (Client)"
sheet_name = "addresses (Client)"
source_table_name = "pat"
sirius_table_name = "persons"


# 1. Get all the columns in the source data table and forget the rest

def get_mapping(excel_doc, sheet_name):
    sheet = pd.read_excel(excel_doc, sheet_name=sheet_name)

    return sheet

mapping = get_mapping(excel_doc=excel_doc, sheet_name=sheet_name)

col_names = mapping[mapping['casrec_table'].str.lower() == source_table_name][
    'casrec_column_name'].tolist()

col_names = [i.split(',') for i in col_names if str(i) != "nan"]
col_names = [item for sublist in col_names for item in sublist]

col_names_string = ", ".join([f"\"{x.strip(' ')}\"" for x in col_names])

conn = psycopg2.connect("host=localhost port=6666 dbname=casrecmigration user=casrec "
                        "password=casrec")
pat_df = pd.read_sql_query(f"select {col_names_string} from etl1.pat limit 3;",conn)
# print(pat_df.to_markdown())

# 2. do the basic remap

def get_simple_mapping(excel_doc, sheet_name):
    sheet = pd.read_excel(excel_doc, sheet_name=sheet_name)
    mapping = {}
    mapping[sheet_name] = {}

    simple_mappings = sheet.fillna("unknown")
    simple_mappings = simple_mappings[simple_mappings[
        'requires_transformation'] == "unknown"]
    simple_mappings = simple_mappings[['column_name', 'casrec_table',
                                       'casrec_column_name', 'requires_transformation']]

    simple_mappings.set_index('column_name', drop=True, inplace=True)
    simple_mappings_dict = simple_mappings.to_dict(orient="index")

    return simple_mappings_dict



def do_simple_remap(simple_mapping_dict, source_table_name, source_data):
    simple_column_remap = [{v['casrec_column_name']: k} for k, v in simple_mapping_dict.items() if v['casrec_table'].lower() == source_table_name and
                           v['casrec_column_name'] != "unknown"]


    columns = {k: v for d in simple_column_remap for k, v in d.items()}
    # pp(columns)

    return source_data.rename(columns=columns)


simple_mapping = get_simple_mapping(excel_doc, sheet_name)

# pp(simple_mapping)

new_df = do_simple_remap(simple_mapping, source_table_name, pat_df)

# print(new_df.to_markdown())

# 3. do some transformations


def get_transformations(excel_doc, sheet_name):
    sheet = pd.read_excel(excel_doc, sheet_name=sheet_name)
    mapping = {}
    mapping[sheet_name] = {}

    transformations = sheet.fillna("unknown")
    transformations = transformations[transformations['requires_transformation'] !=
                                      'unknown']
    transformations = transformations[['column_name', 'casrec_table',
                                       'casrec_column_name', 'requires_transformation']]

    transformations.set_index('column_name', drop=True, inplace=True)
    transformations_dict = transformations.to_dict(orient="index")

    t = {}
    for k, v in transformations_dict.items():
        transforamtion_name = v['requires_transformation']
        original_columns_as_list = v['casrec_column_name'].split(',')
        cols_to_transform = {
            "original_columns": [x.strip() for x in original_columns_as_list],
            "aggregate_col": k
        }

        if transforamtion_name in t:
            t[transforamtion_name].append(cols_to_transform)
        else:
            t[transforamtion_name] = [cols_to_transform]

    return t


transformations = get_transformations(excel_doc, sheet_name)

# pp(transformations)

def squash_columns(cols_to_squash, new_col, df, drop_original_cols=True):
    df[new_col] = df[cols_to_squash].values.tolist()
    # df[new_col] = df[cols_to_squash].to_json(orient='values')

    df[new_col] = df[new_col].apply(lambda x: json.dumps(x))

    if drop_original_cols:
        df = df.drop(columns=cols_to_squash)

    return df

def convert_to_bool(original_col, new_col, df, drop_original_col=True):
    df[new_col] = df[original_col] == "1.0"
    if drop_original_col:
        df = df.drop(columns=original_col)
    return df

def unique_number(new_col, df, length=12):
    # df[new_col] = df.apply(lambda _: uuid.uuid4(), axis=1)
    df[new_col] = df.apply(lambda x: random.randint(10**(length-1),10**length-1),
                           axis = 1)

    return df



transformed_df = new_df
if len(transformations) > 0:
    if 'squash_columns' in transformations:
        for t in transformations['squash_columns']:
            transformed_df = squash_columns(t['original_columns'], t['aggregate_col'],
                                        transformed_df)
    if 'convert_to_bool' in transformations:
        for t in transformations['convert_to_bool']:
            transformed_df = convert_to_bool(t['original_columns'], t['aggregate_col'],
                                        transformed_df)
    if 'unique_number' in transformations:
        for t in transformations['unique_number']:
            transformed_df = unique_number(t['aggregate_col'], transformed_df)
else:
    transformed_df = new_df


# print(transformed_df.to_markdown())

# 4. Fill in any unmapped but required columns

def get_required_columns(excel_doc, sheet_name):
    sheet = pd.read_excel(excel_doc, sheet_name=sheet_name)
    mapping = {}
    mapping[sheet_name] = {}

    required_columns = sheet.fillna("unknown")
    required_columns = required_columns[required_columns['is_pk'] != True]
    required_columns = required_columns[required_columns['nullable'] == False]
    required_columns = required_columns[required_columns['autoincrement'] == False]
    required_columns = required_columns[required_columns['requires_transformation'] == "unknown"]
    required_columns = required_columns[required_columns['casrec_column_name'] == "unknown"]
    required_columns = required_columns[required_columns['default'] == "unknown"]
    required_columns = required_columns[['column_name', 'data_type', 'default_value']]
    # print(required_columns)

    required_columns.set_index('column_name', drop=True, inplace=True)
    required_columns_dict = required_columns.to_dict(orient="index")

    return required_columns_dict


required_columns = get_required_columns(excel_doc, sheet_name)
# pp(required_columns)

for col, details in required_columns.items():
    transformed_df[col] = details['default_value']

# print(transformed_df.to_markdown())


# 5. compare with sirius table structure

def get_sirius_table_columns(excel_doc, sheet_name):
    sheet = pd.read_excel(excel_doc, sheet_name=sheet_name)
    return sheet['column_name'].to_list()

sirius_table_columns = get_sirius_table_columns(excel_doc, sheet_name)
sirius_table = pd.DataFrame(columns=sirius_table_columns)

# print(sirius_table.equals(transformed_df))
#
# print(sirius_table.columns)
# print(new_df.columns)

# 6. insert the unique id based on existing sirius table

from sqlalchemy import create_engine
sirius_engine = create_engine('postgresql://api:api@0.0.0.0:5555/api')
# sirius_db = psycopg2.connect("host=localhost port=5555 dbname=api user=api "
                     # "password=api")

query = f"select max(id) from {sirius_table_name};"
max_id = sirius_engine.execute(query).fetchall()
next_id = max_id[0][0] +1

transformed_df.insert(0, 'id', range(next_id, next_id + len(
    transformed_df)))

print(f"This is what would be inserted into the sirius {sirius_table_name} table:")
print(transformed_df.to_markdown())

# 6. insert into sirius database
# transformed_df.to_sql('addresses', sirius_engine, if_exists='append', index=False)
# transformed_df.to_sql(sirius_table_name, sirius_engine, if_exists='append', index=False)
