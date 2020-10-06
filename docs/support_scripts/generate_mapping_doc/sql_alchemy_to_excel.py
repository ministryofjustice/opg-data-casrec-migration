import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import inspect

writer = pd.ExcelWriter('sirius_tables.xlsx', engine='xlsxwriter')

engine = create_engine('postgresql://api:api@0.0.0.0:5555/api')

ins = inspect(engine)


def convert_default(default_string):
    if default_string == 'false':
        default = False
    elif default_string == 'true':
        default = True
    elif default_string is not None and 'NULL' in default_string:
        default = None
    else:
        default = None
    return default

def convert_length(type_string):
    try:
        return type_string.length
    except:
        return None


def convert_format(type, default_string):
    if type.python_type.__name__ == 'datetime':
        try:
            if default_string.split('::')[1] == 'timestamp without time zone':
                format = '%d/%m/%Y %H:%M'
            else:
                format = None
        except:
            format = None
    elif type.python_type.__name__ == 'date':
        format = '%Y-%m-%d'
    else:
        format = None

    return format

def primary_key(table_name, column_name):

    pk_list = ins.get_pk_constraint(table_name)['constrained_columns']
    if column_name['name'] in pk_list:
        return True
    else:
        return False


def foreign_keys():
    fks = []
    for table_name in ins.get_table_names():
        for key in ins.get_foreign_keys(table_name):
            # print(key)
            if key['referred_table'] != table_name:
                details = f"parent: {key['referred_table']}->" \
                          f"{', '.join(key['referred_columns'])}, " \
                          f"child: {table_name}->" \
                          f"{', '.join(key['constrained_columns'])}"
                p = {
                    "parent": key['referred_table'],
                    "parent_col": key['referred_columns'],
                    "child": table_name,
                    "child_col": key['constrained_columns'],
                    "details":details
                }
                if p not in fks:
                    fks.append(p)
    return fks

fk_list = foreign_keys()

def convert_fk_children(current_table, current_col):
    children = []
    if current_table in [x['parent'] for x in fk_list]:
        for x in fk_list:
            if x['parent'] == current_table:
                if current_col in x['parent_col']:
                    children.append(f"{x['child']}:{', '.join(x['child_col'])}")

    return '\n'.join(children)

def convert_fk_parents(current_table, current_col):
    parents = []
    if current_table in [x['child'] for x in fk_list]:
        for x in fk_list:
            if x['child'] == current_table and current_col in x['child_col']:
                parents.append(f"{x['parent']}:{', '.join(x['parent_col'])}")

    return '\n'.join(parents)


def build_class(tables):

    classes = []


    for table_name in tables:

        new_class = {}
        new_class["name"] = table_name
        new_class["attr"] = []


        columns = ins.get_columns(table_name)
        for col in columns:
            # print(col)

            class_attr = {
                "column_name": col['name'],
                "data_type": col['type'].python_type.__name__,
                "default": convert_default(col['default']),
                "length": convert_length(col["type"]),
                "format": convert_format(col["type"], str(col["default"])),
                "nullable": col['nullable'],
                "autoincrement": col['autoincrement'],
                "is_pk": primary_key(table_name, col),
                "comments": col['comment'],
                "fk_children": convert_fk_children(table_name, col['name']),
                'fk_parents': convert_fk_parents(table_name, col['name']),
                "calculated": "",
                "casrec_table": "",
                "casrec_column_name": "",
                "casrec_data_type": "",
                "casrec_default": "",
                "casrec_length": "",
                "casrec_format": "",
                "casrec_unique_key": "",
                "requires_transformation": "",
                "default_value": "",
            }

            new_class["attr"].append(class_attr)


        classes.append(new_class)




    return classes



tables = ['persons', 'cases', 'person_caseitem', 'notes', 'caseitem_note', 'addresses']
table_dicts = build_class(tables)

for table in table_dicts:
    name = table['name']
    df = pd.DataFrame.from_dict(table['attr'])
    df.to_excel(writer, sheet_name=name, index=False, freeze_panes=(1,0))



writer.save()
