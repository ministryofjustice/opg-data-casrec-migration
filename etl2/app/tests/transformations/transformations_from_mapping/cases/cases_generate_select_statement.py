from pytest_cases import case


@case(id="cases mapping")
def case_mapping_cases():
    mapping = {
        "simple_mapping": {
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
        },
        "transformations": {
            "unique_number": [{"original_columns": ["unknown"], "aggregate_col": "uid"}]
        },
        "required_columns": {"type": {"data_type": "str", "default_value": "order"}},
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


@case(id="cases persons clients")
def case_mapping_persons_client():
    mapping = {
        "simple_mapping": {
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
        },
        "transformations": {
            "date_format_standard": [
                {"original_columns": ["DOB"], "aggregate_col": "dob"}
            ],
            "unique_number": [
                {"original_columns": ["unknown"], "aggregate_col": "uid"}
            ],
        },
        "required_columns": {
            "correspondencebypost": {"data_type": "bool", "default_value": False},
            "correspondencebyphone": {"data_type": "bool", "default_value": False},
            "correspondencebyemail": {"data_type": "bool", "default_value": False},
            "type": {"data_type": "str", "default_value": "actor_client"},
        },
    }

    source_table_name = "pat"
    additional_columns = []

    expected_result = """
        SELECT
            "DOB" as "DOB",
            "Title" as "Title",
            "Forename" as "Forename",
            "Surname" as "Surname",
            "Create" as "Create",
            "Case" as "Case",
            "rct" as "rct"
        FROM etl1.pat ;
    """

    return (mapping, source_table_name, additional_columns, expected_result)
