from pytest_cases import case


@case(id="cases mapping")
def case_mapping_cases():
    mapping = {
        "orderdate": {
            "casrec_table": "ORDER",
            "casrec_column_name": "Made Date",
            "alias": "Made Date",
        },
        "orderissuedate": {
            "casrec_table": "ORDER",
            "casrec_column_name": "Issue Date",
            "alias": "Issue Date",
        },
        "orderexpirydate": {
            "casrec_table": "ORDER",
            "casrec_column_name": "Made Date",
            "alias": "Made Date 1",
        },
        "statusdate": {
            "casrec_table": "ORDER",
            "casrec_column_name": "Made Date",
            "alias": "Made Date 2",
        },
        "caserecnumber": {
            "casrec_table": "ORDER",
            "casrec_column_name": "Case",
            "alias": "Case",
        },
        "ordersubtype": {
            "casrec_table": "ORDER",
            "casrec_column_name": "Ord Type",
            "alias": "Ord Type",
        },
        "casrec_id": {
            "casrec_table": "order",
            "casrec_column_name": "rct",
            "alias": "rct",
        },
        "uid": {
            "casrec_table": "",
            "casrec_column_name": "",
            "new_column": "uid",
            "transformation": "unique_number",
        },
        "type": {
            "casrec_table": "",
            "casrec_column_name": "",
            "default_value": "order",
        },
    }

    source_table_name = "order"
    additional_columns = ["Order No"]

    expected_result = """
        SELECT
            "Made Date" as "Made Date",
            "Issue Date" as "Issue Date",
            "Made Date" as "Made Date 1",
            "Made Date" as "Made Date 2",
            "Case" as "Case",
            "Ord Type" as "Ord Type",
            "rct" as "rct",
            "Order No" as "c_order_no"
        FROM etl1.order;
    """

    return (mapping, source_table_name, additional_columns, expected_result)


@case(id="persons clients mapping")
def case_mapping_persons_client():
    mapping = {
        "salutation": {
            "casrec_table": "PAT",
            "casrec_column_name": "Title",
            "alias": "Title",
        },
        "firstname": {
            "casrec_table": "PAT",
            "casrec_column_name": "Forename",
            "alias": "Forename",
        },
        "surname": {
            "casrec_table": "PAT",
            "casrec_column_name": "Surname",
            "alias": "Surname",
        },
        "createddate": {
            "casrec_table": "PAT",
            "casrec_column_name": "Create",
            "alias": "Create",
        },
        "caserecnumber": {
            "casrec_table": "PAT",
            "casrec_column_name": "Case",
            "alias": "Case",
        },
        "casrec_id": {
            "casrec_table": "pat",
            "casrec_column_name": "rct",
            "alias": "rct",
        },
        "dob": {
            "casrec_table": "pat",
            "casrec_column_name": "DOB",
            "transformation": "date_format_standard",
        },
        "uid": {
            "casrec_table": "",
            "casrec_column_name": "",
            "new_column": "uid",
            "transformation": "unique_number",
        },
        "type": {
            "casrec_table": "",
            "casrec_column_name": "",
            "default_value": "actor_client",
        },
    }

    source_table_name = "pat"
    additional_columns = []

    expected_result = """
        SELECT
            "Title" as "Title",
            "Forename" as "Forename",
            "Surname" as "Surname",
            "Create" as "Create",
            "Case" as "Case",
            "rct" as "rct",
            "DOB" as "DOB"
        FROM etl1.pat;
    """

    return (mapping, source_table_name, additional_columns, expected_result)


@case(id="addresses clients mapping")
def case_mapping_addresses_client():
    mapping = {
        "casrec_id": {
            "alias": "rct",
            "casrec_column_name": "rct",
            "casrec_table": "pat",
        },
        "county": {
            "alias": "Adrs5",
            "casrec_column_name": "Adrs5",
            "casrec_table": "PAT",
        },
        "postcode": {
            "alias": "Postcode",
            "casrec_column_name": "Postcode",
            "casrec_table": "PAT",
        },
        "town": {
            "alias": "Adrs4",
            "casrec_column_name": "Adrs4",
            "casrec_table": "PAT",
        },
        "isairmailrequired": {
            "casrec_column_name": "Foreign",
            "casrec_table": "PAT",
            "transformation": "convert_to_bool",
        },
        "address_lines": {
            "casrec_column_name": ["Adrs1", "Adrs2", "Adrs3"],
            "casrec_table": "PAT",
            "transformation": "squash_columns",
        },
    }

    source_table_name = "pat"
    additional_columns = ["Case"]

    expected_result = """
        SELECT
            "Adrs1" as "Adrs1",
            "Adrs2" as "Adrs2",
            "Adrs3" as "Adrs3",
            "Adrs4" as "Adrs4",
            "Adrs5" as "Adrs5",
            "Postcode" as "Postcode",
            "Foreign" as "Foreign",
            "rct" as "rct",
            "Case" as "c_case"
        FROM etl1.pat;
    """

    return (mapping, source_table_name, additional_columns, expected_result)
