import psycopg2
from sqlalchemy import create_engine

import transformations
from mapping import Mapping
from source_data import SourceData
from table_config import definitions, excel_doc

debug_mode = True
sheet_name = "addresses (Client)"
source_table_name = definitions[sheet_name]['source_table_name']
sirius_table_name = definitions[sheet_name]['sirius_table_name']

casrec_db_connection = psycopg2.connect("host=localhost port=6666 dbname=casrecmigration user=casrec password=casrec")
sirius_engine = create_engine('postgresql://api:api@0.0.0.0:5555/api')

if __name__ == '__main__':
    """
    Step 1 - load the mapping details from the spreadsheet
    """
    mapping_from_excel = Mapping()
    mapping_df = mapping_from_excel.mapping_df(file_name=excel_doc,
                                              sheet_name=sheet_name,
                                       source_table_name=source_table_name)
    mapping_definitions = mapping_from_excel.mapping_definitions(mapping_df=mapping_df)

    """
    Step 2 - get the source data from casrec
    """
    source_data = SourceData()
    source_data_query = source_data.generate_select_string(mapping=mapping_df,
                                                           source_table_name=source_table_name, limit=3)

    source_data_df = source_data.get_source_data(query=source_data_query, db_conn=casrec_db_connection)

    if debug_mode:
        print("\n\nStep 2 - source_data_df:")
        print(source_data_df.to_markdown())

    """
    Step 3 - perform the simple 1-1 mappings
    """

    simple_mapping = mapping_definitions['simple_mapping']

    if len(simple_mapping) > 0:
        simple_mapping_df = transformations.do_simple_remap(
            simple_mapping_dict=simple_mapping, source_table_name=source_table_name,
            source_data=source_data_df)
    else:
        simple_mapping_df = source_data_df

    if debug_mode:
        print("\n\nStep 3 - simple_mapping_df:")
        print(simple_mapping_df.to_markdown())

    """
    Step 4 - perform the standard transformations
    """

    transformation_mapping = mapping_definitions['transformations']

    if len(transformation_mapping) > 0:
        transformed_df = transformations.do_transformations(df=simple_mapping_df,
                                                        transformations=transformation_mapping)
    else:
        transformed_df = simple_mapping_df

    if debug_mode:
        print("\n\nStep 4 - transformed_df:")
        print(transformed_df.to_markdown())


    """
    Step 5 - fill in required columns
    """

    required_columns = mapping_definitions['required_columns']

    if len(required_columns) > 0:
        required_cols_df = transformations.populate_required_columns(df=transformed_df,
                                                                 required_cols=required_columns)
    else:
        required_cols_df = transformed_df

    if debug_mode:
        print("\n\nStep 5 - required_cols_df:")
        print(required_cols_df.to_markdown())

    """
    Step 6 - add unique id based on destination table
    """

    next_id = transformations.get_next_sirius_id(engine=sirius_engine,
                                                 sirius_table_name=sirius_table_name)
    unique_column_name = 'id'

    unique_id_df = transformations.add_incremental_ids(df=transformed_df,
                                                       column_name=unique_column_name,
                                                       starting_number=next_id)

    if debug_mode:
        print("\n\nStep 6 - unique_id_df:")
        print(unique_id_df.to_markdown())

    """
    Step 7 - add migrated flag
    """

    migrated_df = unique_id_df
    migrated_df['from_casrec'] = True

    if debug_mode:
        print("\n\nStep 7 - migrated_df:")
        print(migrated_df.to_markdown())


    """
    Step 8 - insert into destination db
    """

    if debug_mode:
        print("\n\nStep 8 - this is what would be inserted into the destination db if we turned debug off:")
        print(migrated_df.to_markdown())
    else:
        migrated_df.to_sql(sirius_table_name, sirius_engine, if_exists='append', index=False)
