from shared.helpers import get_mapped_fields_per_file


def test_get_mapped_fields_per_file():
    result = get_mapped_fields_per_file(file_name="client_persons_mapping")

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

    assert result == expected_result
