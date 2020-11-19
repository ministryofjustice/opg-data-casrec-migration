from pytest_cases import case


module_name = "cases"
source_table = "order"
destination_table = "cases"


@case(tags="simple")
def case_cases_1(get_config):
    simple_matches = {
        # "Ord Type": ["casesubtype"],  # actually a lookup
        "Made Date": ["orderdate"],
        "Issue Date": ["orderissuedate"],
        # "Ord Stat": ["orderstatus"],  # actually a transformation
        "Case": ["caserecnumber"],
        "Spvn Received": ["receiptdate"],
        "Expiry Date": ["orderexpirydate"],
        # "Ord Type": ["ordersubtype"],  # actualy a lookup
        "Clause Expiry": ["clauseexpirydate"],
    }
    merge_columns = {"source": "Order No", "transformed": "c_order_no"}

    config = get_config

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
def case_cases_2(get_config):
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

    config = get_config
    source_columns = [f'"{x}"' for x in defaults.keys()]

    source_query = f"""
        SELECT
            {', '.join(source_columns)}
        FROM {config.etl2_schema}.{destination_table}
    """

    return (defaults, source_query, module_name)


# @case(tags="lookups")
# def case_casess_3(get_config):
#     lookup_fields = {
#         "Ord Type": {
#             "casesubtype": get_lookup_dict(file_name="order_type_lookup")
#         },
#         "Ord Type": {
#             "ordersubtype": get_lookup_dict(file_name="order_subtype_lookup")
#         }
#     }
#     merge_columns = {"source": "Case", "transformed": "caserecnumber"}
#
#     config = get_config
#
#     source_columns = [f'"{x}"' for x in lookup_fields.keys()]
#     transformed_columns = [f'"{y}"' for x in lookup_fields.values() for y in x]
#
#     source_query = f"""
#         SELECT
#             "{merge_columns['source']}",
#             {', '.join(source_columns)}
#         FROM {config.etl1_schema}.{source_table}
#     """
#
#     transformed_query = f"""
#         SELECT
#             {merge_columns['transformed']},
#             {', '.join(transformed_columns)}
#         FROM {config.etl2_schema}.{destination_table}
#     """
#
#     return (lookup_fields, merge_columns, source_query, transformed_query, module_name)
