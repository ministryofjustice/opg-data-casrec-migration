import logging

log = logging.getLogger("root")


def clear_tables(db_engine, db_config, tables):
    schema = db_config["target_schema"]

    for table in tables.keys():
        drop_statement = f"DROP TABLE IF EXISTS {schema}.{table};"
        try:
            with db_engine.connect() as conn:
                conn.execute(drop_statement)
        except Exception as e:
            log.error(f"There was an error dropping table {table} in {schema}")
            log.debug(e)
            break
