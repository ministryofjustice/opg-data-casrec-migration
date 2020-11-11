import pandas as pd
import os

from config import CasrecMigConfig, SiriusConfig, load_env_vars
from sqlalchemy import create_engine
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

def get_single_sql_value(engine, sql):
    results = engine.execute(sql)
    for r in results:
        return_value = r.values()[0]
        return return_value

load_env_vars()

environment = os.environ.get("ENVIRONMENT")

if environment in ("local", "development"):
    print("-- Running LOAD --")
    migration_db_engine = create_engine(CasrecMigConfig.connection_string)
    sirius_db_engine = create_engine(SiriusConfig.connection_string)

    print("Updating the skeleton clients")
    print("- Clients")
    sql = (
        "SELECT "
        "sirius_id, firstname, surname, createddate, type, caserecnumber "
        "FROM etl3.persons "
        "WHERE sirius_id IS NOT NULL "
        "ORDER BY sirius_id DESC LIMIT 10"
    )
    persons_df = pd.read_sql_query(sql, con=migration_db_engine, index_col=None)
    persons_df = persons_df.rename(columns={"sirius_id": "id"})
    persons_df["clientsource"] = "CASRECMIGRATION"

    print(persons_df)

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
            "clientsource": String(255),
            "supervisioncaseowner_id": Integer,
        },
    )

    updatesql = (
        "UPDATE persons "
        "SET firstname = migrated.firstname, "
        "surname = migrated.surname, "
        "clientsource = migrated.clientsource "
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
    addresses_df = pd.read_sql_query(sql, con=migration_db_engine, index_col=None)
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
    sql = (
        "UPDATE addresses_migrated SET address_lines = (address_lines #>> '{}')::jsonb;"
    )
    sirius_db_engine.execute(sql)

    updatesql = (
        "UPDATE addresses "
        "SET address_lines = migrated.address_lines, "
        "town = migrated.town "
        "FROM addresses_migrated migrated "
        "WHERE migrated.id = addresses.id"
    )

    sirius_db_engine.execute(updatesql)

    # print("- Cases")
    # sql = "SELECT *" "FROM etl3.cases " "WHERE sirius_id IS NOT NULL "
    # cases_df = pd.read_sql_query(sql, con=migration_db_engine, index_col=None)
    # cases_df = cases_df.drop(["id", "c_order_no"], axis=1)
    # cases_df = cases_df.rename(columns={"sirius_id": "id"})
    # cases_df = cases_df.rename(columns={"sirius_client_id": "client_id"})
    # cases_df = cases_df.rename(columns={"ordersubtype": "casesubtype"})
    # cases_df["casetype"] = cases_df["type"].str.upper()
    # print(cases_df)
    # cases_df.to_sql(
    #     "cases_migrated",
    #     sirius_db_engine,
    #     if_exists="replace",
    #     index=False,
    #     chunksize=500,
    #     dtype={
    #         "id": Integer(),
    #         "client_id": Integer(),
    #         "uid": BigInteger,
    #         "type": String(255),
    #         "casetype": String(255),
    #         "casesubtype": String(255),
    #         "caserecnumber": String(255),
    #         "orderdate": Date,
    #         "orderissuedate": Date,
    #         "orderexpirydate": Date,
    #         "statusdate": Date,
    #     },
    # )

    print("Adding new clients")
    print("- Clients")

    sql = "SELECT MAX(uid) FROM persons"
    max_person_uid = get_single_sql_value(sirius_db_engine, sql)

    sql = (
        "SELECT "
        "firstname, surname, createddate, type, caserecnumber "
        "FROM etl3.persons "
        "WHERE sirius_id IS NULL "
        "ORDER BY id ASC"
    )
    persons_df = pd.read_sql_query(sql, con=migration_db_engine, index_col=None)
    persons_df["correspondencebypost"] = 0
    persons_df["correspondencebyphone"] = 0
    persons_df["correspondencebyemail"] = 0
    persons_df["clientsource"] = "CASRECMIGRATION"
    persons_df["uid"] = list(range(max_person_uid+1,max_person_uid+991,1))

    print(persons_df)

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
        con=migration_db_engine,
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
    migration_db_engine.execute(sql)

    print("- Addresses")
    sql = (
        "SELECT sirius_person_id, address_lines, town, county, postcode, isairmailrequired "
        "FROM etl3.addresses "
        "WHERE sirius_id IS NULL"
    )
    addresses_df = pd.read_sql_query(sql, con=migration_db_engine, index_col=None)
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

    # print("- Cases")
    # # needs an index
    # sql = """UPDATE etl3.cases
    #         SET sirius_client_id = map.id
    #         FROM etl3.sirius_map_persons map
    #         WHERE map.caserecnumber = cases.caserecnumber"""
    # migration_db_engine.execute(sql)
    #
    # sql = (
    #     "SELECT *"
    #     "FROM etl3.cases "
    #     "WHERE sirius_id IS NULL "
    #     "AND orderdate IS NOT NULL "
    #     "AND orderissuedate IS NOT NULL "
    #     "AND orderexpirydate IS NOT NULL "
    #     "AND statusdate IS NOT NULL "
    #     "AND orderdate != '' "
    #     "AND orderissuedate != '' "
    #     "AND orderexpirydate != '' "
    #     "AND statusdate != '' "
    # )  # There are nulls in the data for dates, but the DB is not null. Something's screwy somewhere
    # # but for now, just select data with no nulls
    # cases_df = pd.read_sql_query(sql, con=migration_db_engine, index_col=None)
    # cases_df = cases_df.drop(["id", "sirius_id", "c_order_no"], axis=1)
    # cases_df = cases_df.rename(columns={"sirius_client_id": "client_id"})
    # cases_df = cases_df.rename(columns={"ordersubtype": "casesubtype"})
    # cases_df["casetype"] = cases_df["type"].str.upper()
    # cases_df.to_sql(
    #     "cases",
    #     sirius_db_engine,
    #     if_exists="append",
    #     index=False,
    #     chunksize=500,
    #     dtype={
    #         "client_id": Integer,
    #         "uid": BigInteger,
    #         "type": String(255),
    #         "casetype": String(255),
    #         "casesubtype": String(255),
    #         "caserecnumber": String(255),
    #         "orderdate": Date,
    #         "orderissuedate": Date,
    #         "orderexpirydate": Date,
    #         "statusdate": Date,
    #     },
    # )
else:
    print(f"Environment '{environment}'not ready to run this stage yet")
