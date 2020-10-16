import time

from sqlalchemy import create_engine
import click

from config import get_config
from database.clear_database import clear_tables
from database.db_insert import InsertData
from tables.cases.cases import insert_cases
from tables.clients.addresses import insert_addresses_clients
from tables.clients.persons import insert_persons_clients
from tables.deputies.addresses import insert_addresses_deputies

from tables.deputies.persons import insert_persons_deputies
from tables.notes.notes import insert_notes
from tables.notes.persons_note import insert_person_notes
from tables.person_case.order_deputy import insert_order_deputy
from tables.person_case.person_caseitem import insert_person_caseitem


config = get_config()

etl2_db_engine = create_engine(config["etl2_db"]["connection_string"])
etl2_db_schema = config["etl2_db"]["schema_name"]


etl2_db = InsertData(db_engine=etl2_db_engine, schema=etl2_db_schema, is_verbose=True)


@click.command()
@click.option("--clear", prompt=False, default=False)
def main(clear):

    if clear:
        clear_tables(config)

    # Clients - personal details
    insert_persons_clients(config, etl2_db)
    insert_addresses_clients(config, etl2_db)

    # Deputies - personal details
    insert_persons_deputies(config, etl2_db)
    insert_addresses_deputies(config, etl2_db)

    # Cases
    insert_cases(config, etl2_db)

    # Join Persons to Cases
    insert_person_caseitem(config, etl2_db)
    insert_order_deputy(config, etl2_db)

    # Notes
    insert_notes(config, etl2_db)

    # Join Notes to Persons
    insert_person_notes(config, etl2_db)


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
