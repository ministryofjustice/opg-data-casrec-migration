import pandas as pd
from pandas.testing import assert_frame_equal

from entities.deputies.deputymapper import map_deputy_subtype


def test_map_deputy_subtype_with_examples():
    # deputytype, firstname and surname are used to set the other columns
    test_df = pd.DataFrame(
        [
            {
                "id": 1,
                "deputytype": "LAY",
                "firstname": "Vone",
                "surname": "Spork",
                "salutation": "Mr",
                "othernames": "Ventafin",
                "note": "Lay deputy => person",
            },
            {
                "id": 2,
                "deputytype": "PRO",
                "firstname": "Majelian",
                "surname": "DeCroscifor",
                "salutation": "Dr",
                "othernames": "Subantafax",
                "note": "PRO deputy with firstname and surname => person",
            },
            {
                "id": 3,
                "deputytype": "PRO",
                "firstname": None,
                "surname": "Big Company",
                "salutation": "Miss",
                "othernames": "Velocipede",
                "note": "PRO deputy without firstname => organisation",
            },
            {
                "id": 4,
                "deputytype": "PRO",
                "firstname": None,
                "surname": None,
                "salutation": "Professor",
                "othernames": "Mandragorian",
                "note": "PRO deputy with no firstname or surname => organisation",
            },
            {
                "id": 5,
                "deputytype": "PA",
                "firstname": "Biffo",
                "surname": "Andalusia",
                "salutation": "Ms",
                "othernames": "Peregrin",
                "note": "PA deputy with firstname and surname => organisation",
            },
            {
                "id": 6,
                "deputytype": "PA",
                "firstname": "",
                "surname": "Baragron Corp",
                "salutation": "Reverend",
                "othernames": "Bargastofon",
                "note": "PA deputy without firstname => organisation",
            },
            {
                "id": 7,
                "deputytype": "PA",
                "firstname": "",
                "surname": "Humalalala Inc",
                "salutation": "Reverend",
                "othernames": "Bargastofon",
                "note": "PA deputy with surname only => organisation",
            },
        ]
    )

    expected = pd.DataFrame(
        [
            {
                "id": 1,
                "deputytype": "LAY",
                "firstname": "Vone",
                "surname": "Spork",
                "salutation": "Mr",
                "othernames": "Ventafin",
                "organisationname": None,
                "deputysubtype": "PERSON",
            },
            {
                "id": 2,
                "deputytype": "PRO",
                "firstname": "Majelian",
                "surname": "DeCroscifor",
                "salutation": "Dr",
                "othernames": "Subantafax",
                "organisationname": None,
                "deputysubtype": "PERSON",
            },
            {
                "id": 3,
                "deputytype": "PRO",
                "firstname": None,
                "surname": None,
                "salutation": None,
                "othernames": None,
                "organisationname": "Big Company",
                "deputysubtype": "ORGANISATION",
            },
            {
                "id": 4,
                "deputytype": "PRO",
                "firstname": None,
                "surname": None,
                "salutation": None,
                "othernames": None,
                "organisationname": None,
                "deputysubtype": "ORGANISATION",
            },
            {
                "id": 5,
                "deputytype": "PA",
                "firstname": None,
                "surname": None,
                "salutation": None,
                "othernames": None,
                "organisationname": "Andalusia",
                "deputysubtype": "ORGANISATION",
            },
            {
                "id": 6,
                "deputytype": "PA",
                "firstname": None,
                "surname": None,
                "salutation": None,
                "othernames": None,
                "organisationname": "Baragron Corp",
                "deputysubtype": "ORGANISATION",
            },
            {
                "id": 7,
                "deputytype": "PA",
                "firstname": None,
                "surname": None,
                "salutation": None,
                "othernames": None,
                "organisationname": "Humalalala Inc",
                "deputysubtype": "ORGANISATION",
            },
        ]
    )

    actual = test_df.apply(map_deputy_subtype, axis=1)

    print(actual.drop(columns=["note"]).to_markdown())
    print(expected.to_markdown())

    assert_frame_equal(expected, actual.drop(columns=["note"]))

    # print examples for verification with UAT
    examples = test_df.join(actual, how="inner", lsuffix=" (in)", rsuffix=" (out)")
    examples = examples.drop(columns=["note (out)", "deputytype (out)"]).rename(
        columns={
            "note (in)": "Note",
            "organisationname": "organisationname (out)",
            "deputysubtype": "deputysubtype (out)",
        }
    )
    columns = examples.columns.tolist()
    columns.remove("Note")
    columns.append("Note")
    print("\n" + examples[columns].to_markdown())
