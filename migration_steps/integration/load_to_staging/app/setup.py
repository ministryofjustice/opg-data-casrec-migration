import json
import os
import sys
import logging

import psycopg2
from psycopg2 import errors

log = logging.getLogger("root")


def insert_base_data(db_config, db_engine):

    # insert default user into assignees
    base_data = {
        "assignees": f"""
        INSERT INTO {db_config['target_schema']}.assignees(id, name, type)
            VALUES
            (10, 'casrec migration', 'default'),
            (1, 'casrec migration', 'default');
        """,
        "bond_providers": f"""
        insert into {db_config['target_schema']}.bond_providers (id, name, oneoffvalue, telephonenumber, emailaddress, webaddress, uid)
            values
                (1,'Howden',21000.00,null,null,'https://www.howdendeputybonds.co.uk','HOWDEN'),
                (2,'Deputy Bond Services (DBS)',21000.00,null,null,'https://www.deputybondservices.co.uk','DBS'),
                (3,'Marsh',16000.00,null,null,null,'MARSH');
        """,
    }
    for name, statement in base_data.items():

        try:
            db_engine.execute(statement)
        except Exception as e:
            log.error(
                f"There was an error inserting the {name} data into {db_config['target_schema']}"
            )
            log.debug(e)
            sys.exit(1)
