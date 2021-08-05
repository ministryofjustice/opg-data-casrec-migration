from helpers import *


def load_fixtures(self, conn_migration, conn_target):
    # print("- Associated cases")
    # sql = "SELECT id, caserecnumber FROM persons ORDER BY id DESC LIMIT 10"
    # persons_fixtures = pd.read_sql_query(sql, con=sirius_db_engine, index_col=None)
    #
    # sql = """
    # SELECT *
    # FROM etl3.cases
    # WHERE caserecnumber
    # IN (SELECT caserecnumber FROM etl3.persons ORDER BY id ASC LIMIT 5)
    # """
    # etl_cases_df = pd.read_sql_query(sql, con=migration_db_engine, index_col=None)
    #
    # cases_df = etl_cases_df.merge(
    #     persons_fixtures,
    #     how="left",
    #     left_on="caserecnumber",
    #     right_on="caserecnumber",
    #     suffixes=["_case", "_person"],
    # )
    #
    # print(etl_cases_df)
    #
    # cases_df = cases_df.drop(
    #     ["id_case", "c_order_no", "sirius_id", "sirius_client_id"], axis=1
    # )
    # cases_df = cases_df.rename(columns={"id_person": "client_id"})
    # cases_df = cases_df.rename(columns={"ordersubtype": "casesubtype"})
    # cases_df["casetype"] = cases_df["type"].str.upper()
    # print(cases_df)
    #
    # cases_df.to_sql(
    #     "cases",
    #     sirius_db_engine,
    #     if_exists="append",
    #     index=False,
    #     dtype={
    #         "orderdate": Date,
    #         "orderissuedate": Date,
    #         "orderexpirydate": Date,
    #         "statusdate": Date,
    #         "caserecnumber": String(255),
    #         "ordersubtype": String(255),
    #         "uid": BigInteger,
    #         "casetype": String(255),
    #         "client_id": Integer,
    #     },
    # )

    # sql = """
    # SELECT client_id, id
    # FROM cases WHERE caserecnumber IN
    # (SELECT caserecnumber FROM persons ORDER BY id DESC LIMIT 5)
    # """
    # person_caseitems_df = etl_cases_df = pd.read_sql_query(
    #     sql, con=sirius_db_engine, index_col=None
    # )
    # person_caseitems_df = person_caseitems_df.rename(columns={"client_id": "person_id"})
    # person_caseitems_df = person_caseitems_df.rename(columns={"id": "caseitem_id"})
    # person_caseitems_df.to_sql(
    #     "person_caseitem",
    #     sirius_db_engine,
    #     if_exists="append",
    #     index=False,
    #     dtype={"person_id": Integer, "case_id": Integer},
    # )

    def fetch_target_ids(config, conn_migration, conn_target):
        print("- Associated cases")
        # schema = config.schemas["integration"]
        # sirius_cases = pd.read_sql_table("cases", con=sirius_db_engine)
        # sirius_cases_keys = sirius_cases[(sirius_cases.casetype == "ORDER")][
        #     ["id", "caserecnumber", "client_id", "casesubtype", "orderdate"]
        # ]
        # sirius_cases_keys.columns = [
        #     "sirius_cases_id",
        #     "sirius_cases_caserecnumber",
        #     "sirius_persons_id",
        #     "sirius_casesubtype",
        #     "orderdate",
        # ]
        # sirius_cases_keys.to_sql(
        #     "sirius_map_cases",
        #     con=etl3_db_engine,
        #     schema=CasrecMigConfig.pre_migrate_schema,
        #     if_exists="replace",
        #     index=False,
        #     dtype={"sirius_persons_id": Integer},
        # )
        # print(sirius_cases_keys)

    def merge_target_ids(config, conn_migration, conn_target):
        print("- Cases & person_caseitem")
        # # anything other than 2 = pfa (CHECK THIS)
        # # 2 = hw
        # sql = """UPDATE etl3.cases cases
        # SET ordersubtype = 'hw'
        # WHERE ordersubtype = '2';
        # UPDATE etl3.sirius_map_cases SET sirius_casesubtype = 'hw' WHERE sirius_casesubtype = '2'"""
        # etl3_db_engine.execute(sql)
        # sql = """UPDATE etl3.cases cases
        # SET ordersubtype = 'pfa'
        # WHERE ordersubtype != 'hw';
        # UPDATE etl3.sirius_map_cases
        # SET sirius_casesubtype = 'pfa'
        # WHERE sirius_casesubtype != 'hw'"""
        # etl3_db_engine.execute(sql)
        #
        # sql = """UPDATE etl3.person_caseitem
        # SET sirius_person_id = persons.sirius_id
        # FROM etl3.persons WHERE persons.id = CAST(person_caseitem.person_id AS INTEGER)"""
        # etl3_db_engine.execute(sql)
        # sql = """UPDATE etl3.cases cases
        # SET sirius_id = map.sirius_cases_id
        # FROM etl3.person_caseitem, etl3.sirius_map_cases map
        # WHERE CAST(person_caseitem.case_id AS INTEGER) = cases.id
        # AND map.sirius_persons_id = person_caseitem.sirius_person_id
        # AND map.sirius_casesubtype = cases.ordersubtype"""
        # etl3_db_engine.execute(sql)
        # sql = """UPDATE etl3.person_caseitem
        # SET sirius_case_id = etl3.cases.sirius_id
        # FROM etl3.cases WHERE cases.id = CAST(person_caseitem.case_id AS INTEGER)"""
        # etl3_db_engine.execute(sql)
        # sql = """UPDATE etl3.cases cases
        # SET sirius_client_id = map.sirius_persons_id
        # FROM etl3.sirius_map_cases map WHERE map.sirius_cases_id = cases.sirius_id"""
        # etl3_db_engine.execute(sql)
