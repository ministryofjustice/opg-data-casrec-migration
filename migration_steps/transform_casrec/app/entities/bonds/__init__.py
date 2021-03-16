import logging

from helpers import log_title

from entities.bonds.bonds import insert_bonds

log = logging.getLogger("root")


def runner(target_db, db_config):
    """
    | Name      | Running Order | Requires |
    | --------- | ------------- | -------- |
    | bonds   | 1               | cases    |
    |           |               |          |
    |           |               |          |

    """

    log.info(log_title(message="bonds"))

    log.debug("insert_bonds")
    insert_bonds(target_db=target_db, db_config=db_config)


if __name__ == "__main__":

    runner()
