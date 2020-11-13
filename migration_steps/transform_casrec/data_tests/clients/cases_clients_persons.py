from pytest_cases import case

from data_tests.helpers import get_lookup_dict

module_name = "client_persons"


@case(tags="simple")
def case_clients_1(get_config):
    simple_matches = {
        # "Title": ["salutation"],
        "DOB": ["dob"],
        "Create": ["createddate"],
        "Forename": ["firstname", "middlenames"],
        "Surname": ["surname"],
        "AKA Name": ["previousnames"],
        # "Marital Status": ["maritalstatus"],
        "Adrs5": ["countryofresidence"],
    }
    merge_columns = {"source": "Case", "transformed": "caserecnumber"}

    config = get_config

    source_columns = [f'"{x}"' for x in simple_matches.keys()]
    transformed_columns = [f'"{y}"' for x in simple_matches.values() for y in x]

    source_query = f"""
        SELECT
            "{merge_columns['source']}",
            {', '.join(source_columns)}
        FROM {config.etl1_schema}.pat
    """

    transformed_query = f"""
        SELECT
            {merge_columns['transformed']},
            {', '.join(transformed_columns)}
        FROM {config.etl2_schema}.persons
        WHERE "type" = 'actor_client'
    """

    return (simple_matches, merge_columns, source_query, transformed_query, module_name)


@case(tags="default")
def case_clients_2(get_config):
    defaults = {
        "type": "actor_client",
        "systemstatus": True,
        "isreplacementattorney": False,
        "istrustcorporation": False,
        "clientstatus": "Active",
        "statusdate": "Todays date",
        "correspondencebywelsh": False,
        "newsletter": False,
        "specialcorrespondencerequirements_audiotape": False,
        "specialcorrespondencerequirements_largeprint": False,
        "specialcorrespondencerequirements_hearingimpaired": False,
        "specialcorrespondencerequirements_spellingofnamerequirescare": False,
        "digital": False,
        "isorganisation": False,
        "casesmanagedashybrid": False,
        "supervisioncaseowner_id": 10,
        "clientsource": "Casrec",
        "updateddate": "Todays date",
    }

    config = get_config
    source_columns = [f'"{x}"' for x in defaults.keys()]

    source_query = f"""
        SELECT
            {', '.join(source_columns)}
        FROM {config.etl2_schema}.persons
    """

    return (defaults, source_query, module_name)


@case(tags="lookups")
# title is commented out because the anon data is wrong so it will never pass
def case_clients_3(get_config):

    lookup_fields = {
        "Marital Status": {
            "maritalstatus": get_lookup_dict(file_name="marital_status_lookup")
        },
        "Accom Type": {
            "clientaccommodation": get_lookup_dict(
                file_name="accommodation_type_lookup"
            )
        },
        # "Title": {"salutation": get_lookup_dict(file_name="title_codes_lookup")}
    }
    merge_columns = {"source": "Case", "transformed": "caserecnumber"}

    config = get_config

    source_columns = [f'"{x}"' for x in lookup_fields.keys()]
    transformed_columns = [f'"{y}"' for x in lookup_fields.values() for y in x]

    source_query = f"""
        SELECT
            "{merge_columns['source']}",
            {', '.join(source_columns)}
        FROM {config.etl1_schema}.pat
    """

    transformed_query = f"""
        SELECT
            {merge_columns['transformed']},
            {', '.join(transformed_columns)}
        FROM {config.etl2_schema}.persons
        WHERE "type" = 'actor_client'
    """

    return (lookup_fields, merge_columns, source_query, transformed_query, module_name)
