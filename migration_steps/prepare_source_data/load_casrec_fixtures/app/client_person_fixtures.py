"""
Dynamic fixtures for the casrec order table for testing client persons
"""

CLIENT_PERSON_FIXTURES = {
    "source_query": 'SELECT "Case" FROM {schema}.pat WHERE "Case" = \'{case}\'',
    "update_query": "UPDATE {schema}.pat SET {set_clause} WHERE {where_clause}",
    "updates": [
        {
            #
            "source_criteria": {"case": "10000037"},
            "set": {"Accom Type": "", "Title": "1"},
        },
        {
            #
            "source_criteria": {"case": "10002625"},
            "set": {"Accom Type": "CR", "Title": "2"},
        },
        {
            #
            "source_criteria": {"case": "10003409"},
            "set": {"Accom Type": "GPH", "Title": "3"},
        },
        {
            #
            "source_criteria": {"case": "10004038"},
            "set": {"Accom Type": "HOS", "Title": "4"},
        },
        {
            #
            "source_criteria": {"case": "10004188"},
            "set": {"Accom Type": "HOT", "Title": "5"},
        },
        {
            #
            "source_criteria": {"case": "10004257"},
            "set": {"Accom Type": "HSP", "Title": "7"},
        },
        {
            #
            "source_criteria": {"case": "10004263"},
            "set": {"Accom Type": "HSP", "Title": "8"},
        },
        {
            #
            "source_criteria": {"case": "10004637"},
            "set": {"Accom Type": "NH", "Title": "9"},
        },
        {
            #
            "source_criteria": {"case": "10004741"},
            "set": {"Accom Type": "OH", "Title": "10"},
        },
        {
            #
            "source_criteria": {"case": "10004879"},
            "set": {"Accom Type": "OTH", "Title": "11"},
        },
        {
            #
            "source_criteria": {"case": "1005934T"},
            "set": {"Accom Type": "PH", "Title": "12"},
        },
        {
            #
            "source_criteria": {"case": "10005243"},
            "set": {"Accom Type": "PT3", "Title": "13"},
        },
        {
            #
            "source_criteria": {"case": "10005433"},
            "set": {"Accom Type": "RCH", "Title": "14"},
        },
        {
            #
            "source_criteria": {"case": "10006413"},
            "set": {"Accom Type": "REN", "Title": "15"},
        },
        {
            #
            "source_criteria": {"case": "10007163"},
            "set": {"Accom Type": "RH", "Title": "17"},
        },
        {
            #
            "source_criteria": {"case": "10007261"},
            "set": {"Accom Type": "FM", "Title": "18"},
        },
        {
            #
            "source_criteria": {"case": "10007877"},
            "set": {"Accom Type": "FM", "Title": "19"},
        },
        {
            #
            "source_criteria": {"case": "10008713"},
            "set": {"Accom Type": "SH", "Title": "20"},
        },
        {
            #
            "source_criteria": {"case": "10009307"},
            "set": {"Accom Type": "LAH", "Title": "21"},
        },
        {
            #
            "source_criteria": {"case": "10010274"},
            "set": {"Accom Type": "NAC", "Title": "22"},
        },
        {
            #
            "source_criteria": {"case": "10011951"},
            "set": {"Accom Type": "SL", "Title": "23"},
        },
        {
            #
            "source_criteria": {"case": "10012240"},
            "set": {"Accom Type": "SEC", "Title": "24"},
        },
        {
            #
            "source_criteria": {"case": "10012643"},
            "set": {"Accom Type": "OH", "Title": "25"},
        },
        {
            #
            "source_criteria": {"case": "10013116"},
            "set": {"Accom Type": "OH", "Title": "26"},
        },
        {
            #
            "source_criteria": {"case": "10013560"},
            "set": {"Accom Type": "OH", "Title": "27"},
        },
        {
            #
            "source_criteria": {"case": "1005934T"},
            "set": {"Accom Type": "OH", "Title": "28"},
        },
        {
            #
            "source_criteria": {"case": "10013583"},
            "set": {"Accom Type": "OH", "Title": "29"},
        },
        {
            #
            "source_criteria": {"case": "10013617"},
            "set": {"Accom Type": "OH", "Title": "30"},
        },
        {
            #
            "source_criteria": {"case": "1001404T"},
            "set": {"Accom Type": "OH", "Title": "31"},
        },
        {
            #
            "source_criteria": {"case": "10014200"},
            "set": {"Accom Type": "OH", "Title": "32"},
        },
        {
            #
            "source_criteria": {"case": "10015094"},
            "set": {"Accom Type": "OH", "Title": "33"},
        },
        {
            #
            "source_criteria": {"case": "10015105"},
            "set": {"Accom Type": "OH", "Title": "34"},
        },
    ],
}
