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
            "set": {"Bond Co": "0", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # Security dispensed with
            "source_criteria": {"case": "13560544"},
            "set": {"Bond Co": "1", "Bond Rqd": "S", "Ord Stat": "Active"},
        },
        {
            # ALBION INSURANCE CO LTD
            "source_criteria": {"case": "10243489"},
            "set": {"Bond Co": "3", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # CGA INSURANCE BROKERS LTD
            "source_criteria": {"case": "13539594"},
            "set": {"Bond Co": "11", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # CO-OPERATIVE INSURANCE SOCIETY LTD
            "source_criteria": {"case": "1126792T"},
            "set": {"Bond Co": "15", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # CO-OPERATIVE INSURANCE SOCIETY LTD
            "source_criteria": {"case": "10215183"},
            "set": {"Bond Co": "21", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # Deputy Bond Services (DBS)
            "source_criteria": {"case": "10064669"},
            "set": {"Bond Co": "22", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # EAGLE STAR INSURANCE CO LTD
            "source_criteria": {"case": "10200685"},
            "set": {"Bond Co": "27", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # ECONOMIC INSURANCE CO LTD
            "source_criteria": {"case": "10154500"},
            "set": {"Bond Co": "30", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # GENERAL ACCIDENT
            "source_criteria": {"case": "10142194"},
            "set": {"Bond Co": "31", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # Marsh Brokers
            "source_criteria": {"case": "95049033"},
            "set": {"Bond Co": "32", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # THE GUARANTEE SOCIETY LTD
            "source_criteria": {"case": "1003019T"},
            "set": {"Bond Co": "33", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # London & Edinburgh Insurance Co Ltd
            "source_criteria": {"case": "10194709"},
            "set": {"Bond Co": "34", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # GUARDIAN ROYAL EXCHANGE ASS. PLC
            "source_criteria": {"case": "10009526"},
            "set": {"Bond Co": "36", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # LEGAL & GENERAL ASS SOCIETY LTD
            "source_criteria": {"case": "10034898"},
            "set": {"Bond Co": "42", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # NORWICH UNION FIRE INS SOCIETY LTD
            "source_criteria": {"case": "94007697"},
            "set": {"Bond Co": "66", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # HCC Insurance Company PMG
            "source_criteria": {"case": "13572764"},
            "set": {"Bond Co": "71", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # ROYAL INSURANCE (UK) LTD
            "source_criteria": {"case": "10015981"},
            "set": {"Bond Co": "75", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # OTHER INSURANCE COMPANY
            "source_criteria": {"case": "10447959"},
            "set": {"Bond Co": "77", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # SUN ALLIANCE & LONDON INS PLC
            "source_criteria": {"case": "13554746"},
            "set": {"Bond Co": "81", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # Zurich Ltd.
            "source_criteria": {"case": "11560126"},
            "set": {"Bond Co": "91", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # Howden
            "source_criteria": {"case": "10028288"},
            "set": {"Bond Co": "12", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
        {
            # Security Bonds Limited
            "source_criteria": {"case": "94055780"},
            "set": {"Bond Co": "92", "Bond Rqd": "Y", "Ord Stat": "Active"},
        },
    ],
}
