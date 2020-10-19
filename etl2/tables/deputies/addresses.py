from logger import custom_logger
from mapping.mapping import Mapping
from transformations import transformations_from_mapping
import pandas as pd


definition = {
    "sheet_name": "addresses (Deputy)",
    "source_table_name": "deputy_address",
    "source_table_additional_columns": ["Dep Addr No"],
    "destination_table_name": "addresses",
}

log = custom_logger()


def insert_addresses_deputies(config, etl2_db):

    mapping_from_excel = Mapping(
        excel_doc=config.mapping_document, table_definitions=definition
    )
    mapping_dict = mapping_from_excel.mapping_definitions()
    source_data_query = mapping_from_excel.generate_select_string_from_mapping()

    source_data_df = pd.read_sql_query(
        sql=source_data_query, con=config.connection_string
    )

    addresses_df = transformations_from_mapping.perform_transformations(
        mapping_dict,
        definition,
        source_data_df,
        config.connection_string,
        config.etl2_schema,
    )

    deputyship_query = f"""
        select "Dep Addr No", "Deputy No"
        from {config.etl1_schema}.deputyship
    """

    deputyship_df = pd.read_sql_query(deputyship_query, config.connection_string)
    deputyship_df = deputyship_df.drop_duplicates(["Dep Addr No", "Deputy No"])

    persons_query = (
        f'select "id", "c_deputy_no" from etl2.persons '
        f"where \"type\" = 'actor_deputy';"
    )
    persons_df = pd.read_sql_query(persons_query, config.connection_string)

    addresses_with_deputyno_df = addresses_df.merge(
        deputyship_df, how="inner", left_on="c_dep_addr_no", right_on="Dep Addr No"
    )

    address_depno_persons_df = addresses_with_deputyno_df.merge(
        persons_df,
        how="inner",
        left_on="Deputy No",
        right_on="c_deputy_no",
        suffixes=["_address", "_person"],
    )

    address_depno_persons_df = address_depno_persons_df.rename(
        columns={"id_address": "id", "id_person": "person_id"}
    )

    etl2_db.insert_data(
        table_name=definition["destination_table_name"], df=address_depno_persons_df
    )
