import time

from tables.persons_client import final as persons_client
from tables.addresses_client import final as addresses_client
from tables.cases import final as cases
from tables.notes import final as notes
from tables.persons_note import final as person_note
from tables.person_caseitem_client import final as person_caseitem
from sqlalchemy import create_engine


from database.db_insert import InsertData

db_engine = create_engine(
    "postgresql://casrec:casrec@0.0.0.0:6666/casrecmigration"  # pragma: allowlist secret
)
db_schema = "etl2"
insert_data = InsertData(db_engine=db_engine, schema=db_schema, is_verbose=True)

if __name__ == "__main__":
    t = time.process_time()

    insert_data.insert_data(table_name="persons", df=persons_client())

    insert_data.insert_data(table_name="addresses", df=addresses_client())

    insert_data.insert_data(table_name="cases", df=cases())

    insert_data.insert_data(table_name="person_caseitem", df=person_caseitem())

    insert_data.insert_data(table_name="notes", df=notes())

    insert_data.insert_data(table_name="person_note", df=person_note())

    print(f"Total time: {round(time.process_time() - t, 2)}")
