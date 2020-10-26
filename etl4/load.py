import pandas as pd
from sqlalchemy import create_engine
from config import CasrecMigConfig, SiriusConfig
from sqlalchemy.types import (
    Integer,
    Text,
    String,
    DateTime,
    Date,
    BigInteger,
    TIMESTAMP,
    Boolean,
    JSON,
)

db_engine = create_engine(CasrecMigConfig.connection_string)
sirius_db_engine = create_engine(SiriusConfig.connection_string)

print("Updating the skeleton clients")
print("- People")
sql = (
    "SELECT "
    "sirius_id, firstname, surname, createddate, type, caserecnumber, correspondencebypost, correspondencebyphone, correspondencebyemail, uid "
    "FROM etl3.persons "
    "WHERE sirius_id IS NOT NULL "
    "ORDER BY sirius_id DESC LIMIT 10"
)
persons_df = pd.read_sql_query(sql, con=db_engine, index_col=None)
persons_df["correspondencebypost"] = persons_df["correspondencebypost"].replace(
    {"True": 1, "False": 0}
)
persons_df["correspondencebyphone"] = persons_df["correspondencebyphone"].replace(
    {"True": 1, "False": 0}
)
persons_df["correspondencebyemail"] = persons_df["correspondencebyemail"].replace(
    {"True": 1, "False": 0}
)
persons_df = persons_df.rename(columns={"sirius_id": "id"})

persons_df.to_sql(
    "persons_migrated",
    sirius_db_engine,
    if_exists="replace",
    index=False,
    chunksize=500,
    dtype={
        "firstname": String(255),
        "surname": String(255),
        "createddate": TIMESTAMP(),
        "type": String(255),
        "caserecnumber": String(255),
        "correspondencebypost": Boolean,
        "correspondencebyphone": Boolean,
        "correspondencebyemail": Boolean,
        "uid": BigInteger,
        "clientsource": String(255),
        "supervisioncaseowner_id": Integer,
    },
)
print(persons_df)

updatesql = (
    "UPDATE persons "
    "SET firstname = migrated.firstname, "
    "surname = migrated.surname "
    "FROM persons_migrated migrated "
    "WHERE migrated.id = persons.id"
)
sirius_db_engine.execute(updatesql)


print("- Addresses")
sql = (
    "SELECT sirius_id, sirius_person_id, address_lines, town, county, postcode, isairmailrequired "
    "FROM etl3.addresses "
    "WHERE sirius_id IS NOT NULL "
)
addresses_df = pd.read_sql_query(sql, con=db_engine, index_col=None)
addresses_df["isairmailrequired"] = addresses_df["isairmailrequired"].replace(
    {"True": 1, "False": 0}
)
addresses_df = addresses_df.rename(columns={"sirius_id": "id"})
addresses_df = addresses_df.rename(columns={"sirius_person_id": "person_id"})
addresses_df.to_sql(
    "addresses_migrated",
    sirius_db_engine,
    if_exists="replace",
    index=False,
    chunksize=500,
    dtype={
        "id": Integer(),
        "person_id": Integer(),
        "address_lines": JSON,
        "town": String(255),
        "county": String(255),
        "postcode": String(255),
        "isairmailrequired": Boolean,
    },
)
print(addresses_df)

# fix escaping in addresses json
sql = "UPDATE addresses_migrated SET address_lines = (address_lines #>> '{}')::jsonb;"
sirius_db_engine.execute(sql)

updatesql = (
    "UPDATE addresses "
    "SET address_lines = migrated.address_lines, "
    "town = migrated.town "
    "FROM addresses_migrated migrated "
    "WHERE migrated.id = addresses.id"
)

sirius_db_engine.execute(updatesql)


print("- Cases")
sql = "SELECT *" "FROM etl3.cases " "WHERE sirius_id IS NOT NULL "
cases_df = pd.read_sql_query(sql, con=db_engine, index_col=None)
cases_df = cases_df.drop(["id", "casrec_id", "c_order_no"], axis=1)
cases_df = cases_df.rename(columns={"sirius_id": "id"})
cases_df = cases_df.rename(columns={"sirius_client_id": "client_id"})
cases_df = cases_df.rename(columns={"ordersubtype": "casesubtype"})
cases_df["casetype"] = cases_df["type"].str.upper()
print(cases_df)
cases_df.to_sql(
    "cases_migrated",
    sirius_db_engine,
    if_exists="replace",
    index=False,
    chunksize=500,
    dtype={
        "id": Integer(),
        "client_id": Integer(),
        "uid": BigInteger,
        "type": String(255),
        "casetype": String(255),
        "casesubtype": String(255),
        "caserecnumber": String(255),
        "orderdate": Date,
        "orderissuedate": Date,
        "orderexpirydate": Date,
        "statusdate": Date,
    },
)


print("Adding new clients")
print("- People")
sql = (
    "SELECT "
    "firstname, surname, createddate, type, caserecnumber, correspondencebypost, correspondencebyphone, correspondencebyemail, uid "
    "FROM etl3.persons "
    "WHERE sirius_id IS NULL "
    "ORDER BY id ASC"
)
persons_df = pd.read_sql_query(sql, con=db_engine, index_col=None)
persons_df["correspondencebypost"] = persons_df["correspondencebypost"].replace(
    {"True": 1, "False": 0}
)
persons_df["correspondencebyphone"] = persons_df["correspondencebyphone"].replace(
    {"True": 1, "False": 0}
)
persons_df["correspondencebyemail"] = persons_df["correspondencebyemail"].replace(
    {"True": 1, "False": 0}
)

persons_df.to_sql(
    "persons",
    sirius_db_engine,
    if_exists="append",
    index=False,
    chunksize=500,
    dtype={
        "firstname": String(255),
        "surname": String(255),
        "createddate": TIMESTAMP(),
        "type": String(255),
        "caserecnumber": String(255),
        "correspondencebypost": Boolean,
        "correspondencebyphone": Boolean,
        "correspondencebyemail": Boolean,
        "uid": BigInteger,
        "clientsource": String(255),
        "supervisioncaseowner_id": Integer,
    },
)

print("Re-fetch Persons IDs")
sql = "SELECT caserecnumber, id FROM persons WHERE type IN ('actor_client','actor_deputy')"
sirius_persons = pd.read_sql_query(sql, con=sirius_db_engine, index_col=None)
sirius_persons.to_sql(
    "sirius_map_persons",
    con=db_engine,
    schema=CasrecMigConfig.etl3_schema,
    if_exists="replace",
    index=False,
    chunksize=500,
    dtype={"caserecnumber": String(255), "id": Integer},
)

# needs an index
sql = """UPDATE etl3.addresses SET sirius_person_id = map.id
    FROM etl3.sirius_map_persons map
    WHERE map.caserecnumber = addresses.caserecnumber"""
db_engine.execute(sql)

print("- Addresses")
sql = (
    "SELECT sirius_person_id, address_lines, town, county, postcode, isairmailrequired "
    "FROM etl3.addresses "
    "WHERE sirius_id IS NULL"
)
addresses_df = pd.read_sql_query(sql, con=db_engine, index_col=None)
addresses_df["isairmailrequired"] = addresses_df["isairmailrequired"].replace(
    {"True": 1, "False": 0}
)
addresses_df = addresses_df.rename(columns={"sirius_person_id": "person_id"})
addresses_df.to_sql(
    "addresses",
    sirius_db_engine,
    if_exists="append",
    index=False,
    chunksize=500,
    dtype={
        "person_id": Integer,
        "address_lines": JSON,
        "town": String(255),
        "county": String(255),
        "postcode": String(255),
        "isairmailrequired": Boolean,
    },
)
# fix escaping in addresses json
sql = "UPDATE addresses SET address_lines = (address_lines #>> '{}')::jsonb;"
sirius_db_engine.execute(sql)

print("- Cases")
# needs an index
sql = """UPDATE etl3.cases
        SET sirius_client_id = map.id
        FROM etl3.sirius_map_persons map
        WHERE map.caserecnumber = cases.caserecnumber"""
db_engine.execute(sql)

sql = (
    "SELECT *"
    "FROM etl3.cases "
    "WHERE sirius_id IS NULL "
    "AND orderdate IS NOT NULL "
    "AND orderissuedate IS NOT NULL "
    "AND orderexpirydate IS NOT NULL "
    "AND statusdate IS NOT NULL "
    "AND orderdate != '' "
    "AND orderissuedate != '' "
    "AND orderexpirydate != '' "
    "AND statusdate != '' "
)  # There are nulls in the data for dates, but the DB is not null. Something's screwy somewhere
# but for now, just select data with no nulls
cases_df = pd.read_sql_query(sql, con=db_engine, index_col=None)
cases_df = cases_df.drop(["id", "sirius_id", "casrec_id", "c_order_no"], axis=1)
cases_df = cases_df.rename(columns={"sirius_client_id": "client_id"})
cases_df = cases_df.rename(columns={"ordersubtype": "casesubtype"})
cases_df["casetype"] = cases_df["type"].str.upper()
cases_df.to_sql(
    "cases",
    sirius_db_engine,
    if_exists="append",
    index=False,
    chunksize=500,
    dtype={
        "client_id": Integer,
        "uid": BigInteger,
        "type": String(255),
        "casetype": String(255),
        "casesubtype": String(255),
        "caserecnumber": String(255),
        "orderdate": Date,
        "orderissuedate": Date,
        "orderexpirydate": Date,
        "statusdate": Date,
    },
)
