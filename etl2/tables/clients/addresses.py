from mapping.mapping import Mapping
from transformations import transformations_from_mapping
import pandas as pd


definition = {
    "sheet_name": "addresses (Client)",
    "source_table_name": "pat",
    "source_table_additional_columns": ["Case"],
    "destination_table_name": "addresses",
}


def insert_addresses_clients(config, etl2_db):

    mapping_from_excel = Mapping(
        excel_doc=config["mapping_document"]["excel_doc"], table_definitions=definition
    )
    mapping_dict = mapping_from_excel.mapping_definitions()
    source_data_query = mapping_from_excel.generate_select_string_from_mapping()

    source_data_df = pd.read_sql_query(
        sql=source_data_query, con=config["etl2_db"]["connection_string"]
    )

    addresses_df = transformations_from_mapping.perform_transformations(
        mapping_dict, definition, source_data_df, config["etl2_db"]
    )

    persons_query = (
        f'select "id", "caserecnumber" from etl2.persons '
        f"where \"type\" = 'actor_client';"
    )
    persons_df = pd.read_sql_query(
        persons_query, config["etl2_db"]["connection_string"]
    )

    persons_df = persons_df[["id", "caserecnumber"]]

    addresses_joined_df = addresses_df.merge(
        persons_df, how="left", left_on="c_case", right_on="caserecnumber"
    )

    addresses_joined_df["person_id"] = addresses_joined_df["id_y"]
    addresses_joined_df = addresses_joined_df.drop(columns=["id_y"])
    addresses_joined_df = addresses_joined_df.rename(columns={"id_x": "id"})

    etl2_db.insert_data(
        table_name=definition["destination_table_name"], df=addresses_joined_df
    )
