from datetime import datetime

import pytest
from pytest_cases import case
import pandas as pd

module_name = "cases"
source_table = "order"
destination_table = "cases"


@pytest.mark.xfail(reason="dates need formatting properly")
@case(tags="simple")
def case_cases_1(test_config):
    simple_matches = {
        "Made Date": ["orderdate"],
        "Issue Date": ["orderissuedate"],
        "Case": ["caserecnumber"],
        "Spvn Received": ["receiptdate"],
        "Expiry Date": ["orderexpirydate"],
        "Clause Expiry": ["clauseexpirydate"],
    }
    merge_columns = {"source": "Order No", "transformed": "c_order_no"}

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
    """

    return (simple_matches, merge_columns, source_query, transformed_query, module_name)


@case(tags="default")
def case_cases_2(test_config):
    defaults = {
        "applicationtype": 0,
        "casetype": "ORDER",
        "caseattorneysingular": 0,
        "caseattorneyjointlyandseverally": 0,
        "caseattorneyjointly": 0,
        "caseattorneyjointlyandjointlyandseverally": 0,
        "caseattorneyactionadditionalinfo": 0,
        "repeatapplication": 0,
        "type": "order",
        "ascertained_by": 1,
        "donorsignaturewitnessed": 0,
        "donorhaspreviouslpas": 0,
        "trustcorporationsignedas": 1,
        "hasrelativetonotice": 0,
        "areallattorneysapplyingtoregister": 0,
        "donorhasotherepas": 0,
        "usesnotifiedpersons": 0,
        "nonoticegiven": 0,
        "notifiedpersonpermissionby": 1,
        "paymentbydebitcreditcard": 0,
        "paymentbycheque": 0,
        "wouldliketoapplyforfeeremission": 0,
        "haveappliedforfeeremission": 0,
        "anyotherinfo": 0,
        "additionalinfodonorsignature": 0,
        "paymentremission": 0,
        "paymentexemption": 0,
        "attorneypartydeclaration": 1,
        "attorneyapplicationassertion": 1,
        "attorneymentalactpermission": 1,
        "attorneydeclarationsignaturewitness": 0,
        "correspondentcomplianceassertion": 1,
        "applicantsdeclaration": 1,
        "applicationhasrestrictions": 0,
        "applicationhasguidance": 0,
        "applicationhascharges": 0,
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
def case_cases_3(test_config):
    lookup_fields = {
        "casesubtype": {"Ord Type": "order_type_lookup"},
        "ordersubtype": {"Ord Type": "order_subtype_lookup"},
    }
    merge_columns = {"source": "Order No", "transformed": "c_order_no"}

    config = test_config

    source_columns = list(set([f'"{y}"' for x in lookup_fields.values() for y in x]))
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
    """

    return (lookup_fields, merge_columns, source_query, transformed_query, module_name)


@case(tags="calculated")
def case_clients_4(test_config):

    # today = datetime.today().strftime("%Y-%m-%d")
    today = pd.Timestamp(2021, 1, 6)

    calculated_fields = {
        "createddate": today,
        "updateddate": today,
    }

    config = test_config
    source_columns = [f'"{x}"' for x in calculated_fields.keys()]

    source_query = f"""
        SELECT
            {', '.join(source_columns)}
        FROM {config.etl2_schema}.{destination_table}
    """

    return (calculated_fields, source_query, module_name)


@case(tags="row_count")
def case_cases_count(test_config):

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
    """

    return (source_query, transformed_query, module_name)


@case(tags="capitalise")
def case_cases_capitalise(test_config):
    capitalised_fields = {
        "Ord Stat": ["orderstatus"],
    }

    config = test_config
    merge_columns = {"source": "Order No", "transformed": "c_order_no"}
    source_columns = [f'"{x}"' for x in capitalised_fields.keys()]
    transformed_columns = [f'"{y}"' for x in capitalised_fields.values() for y in x]

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
    """

    return (
        capitalised_fields,
        source_query,
        transformed_query,
        merge_columns,
        module_name,
    )
