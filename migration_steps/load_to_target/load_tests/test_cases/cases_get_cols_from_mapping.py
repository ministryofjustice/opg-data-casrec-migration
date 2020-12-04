from pytest_cases import case


@case(id="all fields returned from test json")
def case_just_file():

    include_columns = []
    exclude_columns = []
    reorder_cols = {}

    expected_result = [
        "id",
        "dob",
        "firstname",
        "surname",
        "createddate",
        "type",
        "systemstatus",
        "isreplacementattorney",
        "istrustcorporation",
        "previousnames",
        "caserecnumber",
        "clientaccommodation",
        "maritalstatus",
        "clientstatus",
        "statusdate",
        "correspondencebywelsh",
        "countryofresidence",
        "newsletter",
        "specialcorrespondencerequirements_audiotape",
        "specialcorrespondencerequirements_largeprint",
        "specialcorrespondencerequirements_hearingimpaired",
        "specialcorrespondencerequirements_spellingofnamerequirescare",
        "digital",
        "isorganisation",
        "clientsource",
        "updateddate",
    ]

    return (include_columns, exclude_columns, reorder_cols, expected_result)


@case(id="exclude everything except 'id'")
def case_just_exclude():

    include_columns = []
    exclude_columns = [
        "dob",
        "firstname",
        "surname",
        "createddate",
        "type",
        "systemstatus",
        "isreplacementattorney",
        "istrustcorporation",
        "previousnames",
        "caserecnumber",
        "clientaccommodation",
        "maritalstatus",
        "clientstatus",
        "statusdate",
        "correspondencebywelsh",
        "countryofresidence",
        "newsletter",
        "specialcorrespondencerequirements_audiotape",
        "specialcorrespondencerequirements_largeprint",
        "specialcorrespondencerequirements_hearingimpaired",
        "specialcorrespondencerequirements_spellingofnamerequirescare",
        "digital",
        "isorganisation",
        "clientsource",
        "updateddate",
    ]
    reorder_cols = {}

    expected_result = ["id"]

    return (include_columns, exclude_columns, reorder_cols, expected_result)


@case(id="include 2 extra columns")
def case_just_include():

    include_columns = ["banana", "chipmunk"]
    exclude_columns = []
    reorder_cols = {}

    expected_result = [
        "id",
        "dob",
        "firstname",
        "surname",
        "createddate",
        "type",
        "systemstatus",
        "isreplacementattorney",
        "istrustcorporation",
        "previousnames",
        "caserecnumber",
        "clientaccommodation",
        "maritalstatus",
        "clientstatus",
        "statusdate",
        "correspondencebywelsh",
        "countryofresidence",
        "newsletter",
        "specialcorrespondencerequirements_audiotape",
        "specialcorrespondencerequirements_largeprint",
        "specialcorrespondencerequirements_hearingimpaired",
        "specialcorrespondencerequirements_spellingofnamerequirescare",
        "digital",
        "isorganisation",
        "clientsource",
        "updateddate",
        "banana",
        "chipmunk",
    ]

    return (include_columns, exclude_columns, reorder_cols, expected_result)


@case(id="exclude and include together")
def case_include_and_exclude():

    include_columns = ["banana", "chipmunk"]
    exclude_columns = [
        "dob",
        "firstname",
        "surname",
        "createddate",
        "type",
        "systemstatus",
        "isreplacementattorney",
        "istrustcorporation",
        "previousnames",
        "caserecnumber",
        "clientaccommodation",
        "maritalstatus",
        "clientstatus",
        "statusdate",
        "correspondencebywelsh",
        "countryofresidence",
        "newsletter",
        "specialcorrespondencerequirements_audiotape",
        "specialcorrespondencerequirements_largeprint",
        "specialcorrespondencerequirements_hearingimpaired",
        "specialcorrespondencerequirements_spellingofnamerequirescare",
        "digital",
        "isorganisation",
        "clientsource",
        "updateddate",
    ]
    reorder_cols = {}

    expected_result = ["id", "banana", "chipmunk"]

    return (include_columns, exclude_columns, reorder_cols, expected_result)


@case(id="reorder single col")
def case_reorder_1():

    include_columns = []
    exclude_columns = []
    reorder_cols = {"firstname": 0}

    expected_result = [
        "firstname",
        "id",
        "dob",
        "surname",
        "createddate",
        "type",
        "systemstatus",
        "isreplacementattorney",
        "istrustcorporation",
        "previousnames",
        "caserecnumber",
        "clientaccommodation",
        "maritalstatus",
        "clientstatus",
        "statusdate",
        "correspondencebywelsh",
        "countryofresidence",
        "newsletter",
        "specialcorrespondencerequirements_audiotape",
        "specialcorrespondencerequirements_largeprint",
        "specialcorrespondencerequirements_hearingimpaired",
        "specialcorrespondencerequirements_spellingofnamerequirescare",
        "digital",
        "isorganisation",
        "clientsource",
        "updateddate",
    ]

    return (include_columns, exclude_columns, reorder_cols, expected_result)


@case(id="reorder multiple col")
def case_reorder_2():

    include_columns = []
    exclude_columns = []
    reorder_cols = {"caserecnumber": 0, "type": 3, "firstname": 4}

    expected_result = [
        "caserecnumber",
        "id",
        "dob",
        "type",
        "firstname",
        "surname",
        "createddate",
        "systemstatus",
        "isreplacementattorney",
        "istrustcorporation",
        "previousnames",
        "clientaccommodation",
        "maritalstatus",
        "clientstatus",
        "statusdate",
        "correspondencebywelsh",
        "countryofresidence",
        "newsletter",
        "specialcorrespondencerequirements_audiotape",
        "specialcorrespondencerequirements_largeprint",
        "specialcorrespondencerequirements_hearingimpaired",
        "specialcorrespondencerequirements_spellingofnamerequirescare",
        "digital",
        "isorganisation",
        "clientsource",
        "updateddate",
    ]

    return (include_columns, exclude_columns, reorder_cols, expected_result)


@case(id="reorder multiple col unordered")
def case_reorder_3():

    include_columns = []
    exclude_columns = []
    reorder_cols = {"caserecnumber": 0, "firstname": 4, "type": 3}

    expected_result = [
        "caserecnumber",
        "id",
        "dob",
        "type",
        "surname",
        "firstname",
        "createddate",
        "systemstatus",
        "isreplacementattorney",
        "istrustcorporation",
        "previousnames",
        "clientaccommodation",
        "maritalstatus",
        "clientstatus",
        "statusdate",
        "correspondencebywelsh",
        "countryofresidence",
        "newsletter",
        "specialcorrespondencerequirements_audiotape",
        "specialcorrespondencerequirements_largeprint",
        "specialcorrespondencerequirements_hearingimpaired",
        "specialcorrespondencerequirements_spellingofnamerequirescare",
        "digital",
        "isorganisation",
        "clientsource",
        "updateddate",
    ]

    return (include_columns, exclude_columns, reorder_cols, expected_result)


@case(id="exclude and include and reorder")
def case_include_and_exclude_and_reorder():

    include_columns = ["banana", "chipmunk"]
    exclude_columns = [
        "dob",
        "firstname",
        "surname",
        "createddate",
        "type",
        "systemstatus",
        "isreplacementattorney",
        "istrustcorporation",
        "previousnames",
        "caserecnumber",
        "clientaccommodation",
        "maritalstatus",
        "clientstatus",
        "statusdate",
        "correspondencebywelsh",
        "countryofresidence",
        "newsletter",
        "specialcorrespondencerequirements_audiotape",
        "specialcorrespondencerequirements_largeprint",
        "specialcorrespondencerequirements_hearingimpaired",
        "specialcorrespondencerequirements_spellingofnamerequirescare",
        "digital",
        "isorganisation",
        "clientsource",
        "updateddate",
    ]
    reorder_cols = {"banana": 0, "id": 2}

    expected_result = ["banana", "chipmunk", "id"]

    return (include_columns, exclude_columns, reorder_cols, expected_result)
