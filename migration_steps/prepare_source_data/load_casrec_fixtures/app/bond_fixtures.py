"""
Dynamic fixtures for the casrec order table for testing bonds
"""

BOND_FIXTURES = {
    "source_query": 'SELECT "Case", "Ord Stat" FROM {schema}.order WHERE "Case" = \'{case}\' and "Ord Stat" = \'Active\'',
    # set an account's fields to fixture values
    "update_query": "UPDATE {schema}.order SET {set_clause} WHERE {where_clause}",
    # casrec accounts with the dates set below will be transformed to
    # Sirius annual_report_log records with the status and reviewstatus shown
    "updates": [
        {
            # No Fidelity CO. code input at this time.
            "source_criteria": {"case": "10207131"},
            "set": {"Bond Co": "0"},
        },
        {
            # Security dispensed with
            "source_criteria": {"case": "13560544"},
            "set": {"Bond Co": "1"},
        },
        {
            # ALBION INSURANCE CO LTD
            "source_criteria": {"case": "10243489"},
            "set": {"Bond Co": "3"},
        },
        {
            # CGA INSURANCE BROKERS LTD
            "source_criteria": {"case": "13539594"},
            "set": {"Bond Co": "11"},
        },
        {
            # CO-OPERATIVE INSURANCE SOCIETY LTD
            "source_criteria": {"case": "1126792T"},
            "set": {"Bond Co": "15"},
        },
        {
            # CO-OPERATIVE INSURANCE SOCIETY LTD
            "source_criteria": {"case": "10215183"},
            "set": {"Bond Co": "21"},
        },
        {
            # Deputy Bond Services (DBS)
            "source_criteria": {"case": "10064669"},
            "set": {"Bond Co": "22"},
        },
        {
            # EAGLE STAR INSURANCE CO LTD
            "source_criteria": {"case": "10200685"},
            "set": {"Bond Co": "27"},
        },
        {
            # ECONOMIC INSURANCE CO LTD
            "source_criteria": {"case": "10154500"},
            "set": {"Bond Co": "30"},
        },
        {
            # GENERAL ACCIDENT
            "source_criteria": {"case": "10142194"},
            "set": {"Bond Co": "31"},
        },
        {
            # Marsh Brokers
            "source_criteria": {"case": "95049033"},
            "set": {"Bond Co": "32"},
        },
        {
            # THE GUARANTEE SOCIETY LTD
            "source_criteria": {"case": "1003019T"},
            "set": {"Bond Co": "33"},
        },
        {
            # London & Edinburgh Insurance Co Ltd
            "source_criteria": {"case": "10194709"},
            "set": {"Bond Co": "34"},
        },
        {
            # GUARDIAN ROYAL EXCHANGE ASS. PLC
            "source_criteria": {"case": "10009526"},
            "set": {"Bond Co": "36"},
        },
        {
            # LEGAL & GENERAL ASS SOCIETY LTD
            "source_criteria": {"case": "10034898"},
            "set": {"Bond Co": "42"},
        },
        {
            # NORWICH UNION FIRE INS SOCIETY LTD
            "source_criteria": {"case": "94007697"},
            "set": {"Bond Co": "66"},
        },
        {
            # HCC Insurance Company PMG
            "source_criteria": {"case": "13572764"},
            "set": {"Bond Co": "71"},
        },
        {
            # ROYAL INSURANCE (UK) LTD
            "source_criteria": {"case": "10015981"},
            "set": {"Bond Co": "75"},
        },
        {
            # OTHER INSURANCE COMPANY
            "source_criteria": {"case": "10447959"},
            "set": {"Bond Co": "77"},
        },
        {
            # SUN ALLIANCE & LONDON INS PLC
            "source_criteria": {"case": "13554746"},
            "set": {"Bond Co": "81"},
        },
        {
            # Zurich Ltd.
            "source_criteria": {"case": "11560126"},
            "set": {"Bond Co": "91"},
        },
        {
            # Howden
            "source_criteria": {"case": "10028288"},
            "set": {"Bond Co": "12"},
        },
        {
            # Security Bonds Limited
            "source_criteria": {"case": "94055780"},
            "set": {"Bond Co": "92"},
        },
    ],
}
