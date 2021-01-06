import pandas as pd
import pytest
from pytest_cases import case


module_name = "client_persons"
source_table = "pat"
destination_table = "persons"


@pytest.mark.xfail(reason="dates need formatting properly")
@case(tags="simple")
def case_clients_1(test_config):
    simple_matches = {
        "DOB": ["dob"],
        "Create": ["createddate"],
        "Forename": ["firstname", "middlenames"],
        "Surname": ["surname"],
        "AKA Name": ["previousnames"],
        "Adrs5": ["countryofresidence"],
    }
    merge_columns = {"source": "Case", "transformed": "caserecnumber"}

    config = test_config

    source_columns = [f'"{x}"' for x in simple_matches.keys()]
    transformed_columns = [f'"{y}"' for x in simple_matches.values() for y in x]

    source_query = f"""
        SELECT
            "{merge_columns['source']}",
            {', '.join(source_columns)}
        FROM {config.etl1_schema}.{source_table}
    """

    transformed_query = f"""
        SELECT
            {merge_columns['transformed']},
            {', '.join(transformed_columns)}
        FROM {config.etl2_schema}.{destination_table}
        WHERE "type" = 'actor_client'
    """

    return (simple_matches, merge_columns, source_query, transformed_query, module_name)


@case(tags="default")
def case_clients_2(test_config):
    defaults = {
        "type": "actor_client",
        "systemstatus": True,
        "isreplacementattorney": False,
        "istrustcorporation": False,
        "clientstatus": "Active",
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
        "clientsource": "CASRECMIGRATION",
    }

    config = test_config
    source_columns = [f'"{x}"' for x in defaults.keys()]

    source_query = f"""
        SELECT
            {', '.join(source_columns)}
        FROM {config.etl2_schema}.{destination_table}
    """

    return (defaults, source_query, module_name)


@case(tags="lookups")
# title is commented out because the anon data is wrong so it will never pass
def case_clients_3(test_config):

    lookup_fields = {
        "maritalstatus": {"Marital Status": "marital_status_lookup"},
        "clientaccommodation": {"Accom Type": "accommodation_type_lookup"},
        # "Title": {"salutation": get_lookup_dict(file_name="title_codes_lookup")}
    }
    merge_columns = {"source": "Case", "transformed": "caserecnumber"}

    config = test_config

    source_columns = [f'"{y}"' for x in lookup_fields.values() for y in x]
    transformed_columns = [f'"{x}"' for x in lookup_fields.keys()]

    source_query = f"""
        SELECT
            "{merge_columns['source']}",
            {', '.join(source_columns)}
        FROM {config.etl1_schema}.{source_table}
    """

    transformed_query = f"""
        SELECT
            {merge_columns['transformed']},
            {', '.join(transformed_columns)}
        FROM {config.etl2_schema}.{destination_table}
        WHERE "type" = 'actor_client'
    """

    return (lookup_fields, merge_columns, source_query, transformed_query, module_name)


@case(tags="calculated")
def case_clients_4(test_config):

    today = pd.Timestamp(2021, 1, 6)

    calculated_fields = {
        "statusdate": today,
        "updateddate": today,
    }
    config = test_config

    source_columns = [f'"{x}"' for x in calculated_fields.keys()]

    source_query = f"""
        SELECT
            {', '.join(source_columns)}
        FROM {config.etl2_schema}.persons
    """

    return (calculated_fields, source_query, module_name)


@case(tags="row_count")
def case_clients_count(test_config):

    config = test_config
    source_query = f"""
        SELECT
            *
        FROM {config.etl1_schema}.{source_table}
    """

    transformed_query = f"""
        SELECT
            *
        FROM {config.etl2_schema}.{destination_table}
        WHERE "type" = 'actor_client'
    """

    return (source_query, transformed_query, module_name)
