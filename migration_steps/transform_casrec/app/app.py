import time
import os

from sqlalchemy import create_engine
import click

from entities import cases, clients, order_deputy, notes, deputies, person_case
from entities.person_case import person_caseitem
from utilities.clear_database import clear_tables
from utilities.db_insert import InsertData

# from entities.cases.cases import insert_cases

from config import get_config

environment = os.environ.get("ENVIRONMENT")

config = get_config(env=environment)

etl2_db_engine = create_engine(config.connection_string)

etl2_db = InsertData(
    db_engine=etl2_db_engine, schema=config.etl2_schema, is_verbose=True
)


@click.command()
@click.option(
    "--clear",
    prompt=False,
    default=False,
    help="Clear existing database " "tables: True or False",
)
@click.option(
    "--entity_list",
    multiple=True,
    prompt=False,
    help="List of entities you want to transform, eg 'clients,deputies,cases'.",
)
def main(clear, entity_list):

    if clear:
        clear_tables(config)

    if entity_list:
        allowed_entities = (entity_list)[0].split(",")

        print(f"Processing entities: {(', ').join(entity_list)}")

    else:
        allowed_entities = []
        print("Processing all entities")

    # Data - each entity can be run independently
    if len(allowed_entities) == 0 or "clients" in allowed_entities:
        clients.runner(config, etl2_db)
    if len(allowed_entities) == 0 or "deputies" in allowed_entities:
        deputies.runner(config, etl2_db)
    if len(allowed_entities) == 0 or "cases" in allowed_entities:
        cases.runner(config, etl2_db)
    if len(allowed_entities) == 0 or "notes" in allowed_entities:
        notes.runner(config, etl2_db)

    # Join tables - rely on other entities to run
    if len(allowed_entities) == 0 or "person_case" in allowed_entities:
        person_case.runner(config, etl2_db)
    if len(allowed_entities) == 0 or "order_deputy" in allowed_entities:
        order_deputy.runner(config, etl2_db)


if __name__ == "__main__":
    t = time.process_time()

    main()

    print(f"Total time: {round(time.process_time() - t, 2)}")
