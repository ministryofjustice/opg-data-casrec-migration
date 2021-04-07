import logging

from table_helpers import check_enabled_by_table_name

log = logging.getLogger("root")


def clear_tables(db_engine, db_config):
    schema = db_config["target_schema"]

    # reset uids in persons and cases
    table_names = ["cases", "persons"]
    for table in table_names:

        if check_enabled_by_table_name(table_name=table):

            uid_reset_statement = f"UPDATE {schema}.{table} SET uid = NULL;"
            try:
                with db_engine.connect() as conn:
                    conn.execute(uid_reset_statement)
            except Exception as e:
                log.error(
                    f"There was an error resetting the uid in {table} in {db_config['target_schema']}"
                )
                log.debug(e)
                break
