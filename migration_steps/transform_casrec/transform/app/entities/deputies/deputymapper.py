import pandas as pd


def map_deputy_subtype(row: pd.Series) -> pd.Series:
    """
    Map deputy subtype (and associated name fields) depending
    on whether this is a Lay, PA or PRO deputy.

    See IN-1118 and IN-1119.

    :param row: Deputy row mapped from casrec to Sirius. The Sirius
        columns are used to complete the mapping (rather than the
        casrec ones).

        Expected columns in row are:
        - deputytype
        - firstname
        - surname

        The following columns are touched, depending on whether the
        row is for a LAY or PA/PRO deputy, and depending
        on which input columns are set (or not):
        - organisationname
        - deputysubtype
        - surname
        - saluation
        - firstname
        - othernames
    """
    row["organisationname"] = None
    row["deputysubtype"] = None

    is_pa_deputy = row["deputytype"] == "PA"
    is_pro_deputy = row["deputytype"] == "PRO"
    is_lay_deputy = row["deputytype"] == "LAY"

    has_firstname = row["firstname"] not in (None, "")
    has_surname = row["surname"] not in (None, "")

    # these rules are derived from IN-1119
    is_organisation = is_pa_deputy or (is_pro_deputy and not has_firstname)
    is_person = is_lay_deputy or (is_pro_deputy and has_firstname and has_surname)

    # deputytype is set from the deputy_type_lookup
    # in the Deputy spreadsheet
    if is_organisation:
        row["deputysubtype"] = "ORGANISATION"

        names = [row["firstname"], row["othernames"], row["surname"]]
        row["organisationname"] = " ".join(filter(None, names))

        row["salutation"] = None
        row["firstname"] = None
        row["othernames"] = None
        row["surname"] = None

    elif is_person:
        row["deputysubtype"] = "PERSON"

    return row
