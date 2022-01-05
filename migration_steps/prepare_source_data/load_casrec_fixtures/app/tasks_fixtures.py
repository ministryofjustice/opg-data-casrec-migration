"""
Dynamic fixtures for the casrec order table for testing tasks
"""

TASKS_FIXTURES = {
    "source_query": 'SELECT "Case" FROM {schema}.sup_activity WHERE "Case" = \'{case}\'',
    # set an account's fields to fixture values
    "update_query": "UPDATE {schema}.sup_activity SET {set_clause} WHERE {where_clause}",
    "updates": [
        {
            # CWGN
            "source_criteria": {"case": "10336709"},
            "set": {"Sup Desc": "handover"},
        },
        {
            # CWGN
            "source_criteria": {"case": "10201193"},
            "set": {"Sup Desc": "Reminder to follow up action on case"},
        },
        {
            # VICO
            "source_criteria": {"case": "95010297"},
            "set": {
                "Sup Desc": "visit to be commissioned on a set date. Also to be furthered on 8 weeks when vi"
            },
        },
        {
            # OEN6
            "source_criteria": {"case": "96400946"},
            "set": {
                "Sup Desc": "Contact D to remind him that a time-limited order will expire shortly."
            },
        },
        {
            # ORRE
            "source_criteria": {"case": "94012682"},
            "set": {
                "Sup Desc": "Review terms of the order to check that they are being complied with"
            },
        },
        {
            # FCNR
            "source_criteria": {"case": "10109755"},
            "set": {"Sup Desc": "Submission of New Deputy Report"},
        },
        {
            # FCIC
            "source_criteria": {"case": "10141254"},
            "set": {"Sup Desc": "First Contact Call to be completed"},
        },
        {
            # "CNC
            "source_criteria": {"case": "10154051"},
            "set": {"Sup Desc": "RRT TEAM USE"},
        },
        {
            # CCUC
            "source_criteria": {"case": "9820277T"},
            "set": {"Sup Desc": "LAY CATCH UP TELEPHONE CALL - general activity"},
        },
        {
            # VIRD
            "source_criteria": {"case": "10096406"},
            "set": {"Sup Desc": "to be set at time of commission for 12 weeks."},
        },
        {
            # CSIC
            "source_criteria": {"case": "10149066"},
            "set": {"Sup Desc": "Settling in call due"},
        },
        {
            # FCQS
            "source_criteria": {"case": "98141395"},
            "set": {"Sup Desc": "Issued FCC questionaire and await return"},
        },
        {
            # CPOD
            "source_criteria": {"case": "95032391"},
            "set": {"Sup Desc": "Activity to prompt proof of death checks etc."},
        },
        {
            # CCUC
            "source_criteria": {"case": "10259249"},
            "set": {"Sup Desc": "LAY CATCH UP CALL"},
        },
        {
            # ORRE
            "source_criteria": {"case": "10246308"},
            "set": {
                "Sup Desc": "Lay Order assessed from Lay deputies copy - Original copy to be verified when received from CoP"
            },
        },
        {
            # RERR
            "source_criteria": {"case": "10292742"},
            "set": {
                "Sup Desc": "Review the annual ficial report. Consider follow-up action."
            },
        },
    ],
}
