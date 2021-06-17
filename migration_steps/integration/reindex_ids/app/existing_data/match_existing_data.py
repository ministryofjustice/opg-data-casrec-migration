import logging
import psycopg2
import os
import sys
from pathlib import Path

from helpers import format_error_message

current_path = Path(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, str(current_path) + "/../../../../shared")
from decorators import timer

log = logging.getLogger("root")


@timer
def match_existing_data(db_config, table_details):
    """
    This is a placeholder for now. Just setting everything as new data for now
    The real matchy script will look WAY more complicated than this!
    """
    default_value = "INSERT"
    log.info(f"(currently just setting every record to '{default_value}')")
    connection_string = db_config["db_connection_string"]
    conn = psycopg2.connect(connection_string)

    for table in table_details:
        log.debug(f"Setting method on {table} to default_value: '{default_value}'")
        query = f"""
            UPDATE {db_config['target_schema']}.{table}
            SET method = '{default_value}';
        """
        cursor = conn.cursor()
        try:
            cursor.execute(query)
        except psycopg2.DatabaseError as e:
            log.error(
                f"error matching existing data - table probably doesn't exist",
                extra={"error": format_error_message(e=e)},
            )
        except Exception as e:
            log.error(e, extra={"error": format_error_message(e=e)})
        finally:
            cursor.close()

            conn.commit()
