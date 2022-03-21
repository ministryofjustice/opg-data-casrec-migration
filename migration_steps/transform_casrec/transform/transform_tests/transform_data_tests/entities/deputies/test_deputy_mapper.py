import pandas as pd
from pandas.testing import assert_frame_equal

from entities.deputies.deputymapper import map_deputy_subtype


def test_map_deputy_subtype_with_examples():
    # deputytype, firstname and surname are used to set the other columns
    test_df = pd.DataFrame(
        [
            {
                # Person: Lay
                "deputytype": "LAY",
                "firstname": "Vone",
                "surname": "Spork",
                "salutation": "Mr",
                "middlenames": "Ventafin",
                "note": "Lay deputy => person",
            },
            {
                # Person: PA with firstname and surname
                "deputytype": "PA",
                "firstname": "Biffo",
                "surname": "Andalusia",
                "salutation": "Ms",
                "middlenames": "Peregrin",
                "note": "PA deputy with firstname and surname => person",
            },
            {
                # Person: PRO with firstname and surname
                "deputytype": "PRO",
                "firstname": "Majelian",
                "surname": "DeCroscifor",
                "salutation": "Dr",
                "middlenames": "Subantafax",
                "note": "PRO deputy with firstname and surname => person",
            },
            {
                # Organisation: PA without firstname
                "deputytype": "PA",
                "firstname": "",
                "surname": "Baragron Corp",
                "salutation": "Reverend",
                "middlenames": "Bargastofon",
                "note": "PA deputy without firstname => organisation",
            },
            {
                "deputytype": "PRO",
                "firstname": None,
                "surname": "Big Company",
                "salutation": "Miss",
                "middlenames": "Velocipede",
                "note": "PRO deputy without firstname => organisation",
            },
            {
                "deputytype": "PRO",
                "firstname": None,
                "surname": None,
                "salutation": "Professor",
                "middlenames": "Mandragorian",
                "note": "PRO deputy with no firstname or surname => organisation",
            },
        ]
    )

    expected = pd.DataFrame(
        [
            {
                "deputytype": "LAY",
                "firstname": "Vone",
                "surname": "Spork",
                "salutation": "Mr",
                "middlenames": "Ventafin",
                "organisationname": None,
                "deputysubtype": "PERSON",
            },
            {
                "deputytype": "PA",
                "firstname": "Biffo",
                "surname": "Andalusia",
                "salutation": "Ms",
                "middlenames": "Peregrin",
                "organisationname": None,
                "deputysubtype": "PERSON",
            },
            {
                "deputytype": "PRO",
                "firstname": "Majelian",
                "surname": "DeCroscifor",
                "salutation": "Dr",
                "middlenames": "Subantafax",
                "organisationname": None,
                "deputysubtype": "PERSON",
            },
            {
                "deputytype": "PA",
                "firstname": None,
                "surname": None,
                "salutation": None,
                "middlenames": None,
                "organisationname": "Baragron Corp",
                "deputysubtype": "ORGANISATION",
            },
            {
                "deputytype": "PRO",
                "firstname": None,
                "surname": None,
                "salutation": None,
                "middlenames": None,
                "organisationname": "Big Company",
                "deputysubtype": "ORGANISATION",
            },
            {
                "deputytype": "PRO",
                "firstname": None,
                "surname": None,
                "salutation": None,
                "middlenames": None,
                "organisationname": None,
                "deputysubtype": "ORGANISATION",
            },
        ]
    )

    actual = test_df.apply(map_deputy_subtype, axis=1)

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
