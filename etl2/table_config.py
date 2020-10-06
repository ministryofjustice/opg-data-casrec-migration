excel_doc = 'mapping_doc.xlsx'

definitions = {
    "persons (Client)": {
        "source_table_name": "pat",
        "sirius_table_name": "persons",
        "does it work?": True
    },
    "persons (Deputy)": {
        "source_table_name": "pat",
        "sirius_table_name": "persons",
        "does it work?": False
    },
    "addresses (Client)": {
        "source_table_name": "pat",
        "sirius_table_name": "addresses",
        "does it work?": True
    },
    "addresses (Deputy)": {
        "source_table_name": "pat",
        "sirius_table_name": "addresses",
        "does it work?": False
    },
    "cases": {
        "source_table_name": "order",
        "sirius_table_name": "cases",
        "does it work?": True
    },
    "person_caseitem (Client)": {
        "source_table_name": "",
        "sirius_table_name": "",
        "does it work?": False
    },
    "person_caseitem (deputy)": {
        "source_table_name": "",
        "sirius_table_name": "",
        "does it work?": False
    },
    "notes": {
        "source_table_name": "remarks",
        "sirius_table_name": "notes",
        "does it work?": True
    },
    "caseitem_note": {
        "source_table_name": "",
        "sirius_table_name": "",
        "does it work?": False
    },
}
