from sqlalchemy import create_engine
import logging
import os

from sqlalchemy.orm import sessionmaker

log = logging.getLogger("root")


def reindex_db(db_config):

    db = db_config["target_db_name"]
    db_engine = create_engine(db_config["target_db_connection_string"])

    reindex_db_statement = f"""
        REINDEX DATABASE {db};
    """

    try:
        session = sessionmaker(bind=db_engine)()
        session.connection().connection.set_isolation_level(0)
        session.execute(reindex_db_statement)
        session.connection().connection.set_isolation_level(1)
    except Exception as e:
        log.error(f"There was an error reindexing db {db}")
        log.debug(e)
        os._exit(1)
