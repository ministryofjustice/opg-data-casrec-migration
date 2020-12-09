import os
import logging
from pathlib import Path
from dotenv import load_dotenv

import custom_logger

log = logging.getLogger("root")
log.addHandler(custom_logger.MyHandler())


def load_env_vars():
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    env_path = current_path / "../.env"
    load_dotenv(dotenv_path=env_path)


class BaseConfig:
    load_env_vars()
    db_config = {
        "migration": {
            "host": os.environ.get("DB_HOST"),
            "port": os.environ.get("DB_PORT"),
            "name": os.environ.get("DB_NAME"),
            "user": os.environ.get("DB_USER"),
            "password": os.environ.get("DB_PASSWORD"),
        },
        "target": {
            "host": os.environ.get("SIRIUS_DB_HOST"),
            "port": os.environ.get("SIRIUS_DB_PORT"),
            "name": os.environ.get("SIRIUS_DB_NAME"),
            "user": os.environ.get("SIRIUS_DB_USER"),
            "password": os.environ.get("SIRIUS_DB_PASSWORD"),
        },
    }

    schemas = {
        "pre_transform": "etl1",
        "post_transform": "etl2",
        "integration": "integration",
        "public": "public",
        "pre_migration": "pre_migration",
    }

    row_limit = 5
    VERBOSE = 5
    DATA = 2
    verbosity_levels = {0: "INFO", 1: "DEBUG", 2: "VERBOSE"}

    def verbose(self, msg, *args, **kwargs):
        if logging.getLogger().isEnabledFor(self.VERBOSE):
            logging.log(self.VERBOSE, msg)

    def custom_log_level(self):
        logging.addLevelName(self.VERBOSE, "VERBOSE")
        logging.Logger.verbose = self.verbose

    def set_logging_level(self, verbose):
        try:
            log.setLevel(self.verbosity_levels[verbose])
            log.info(f"{self.verbosity_levels[verbose]} logging enabled")
        except KeyError:
            log.setLevel("INFO")
            log.info(f"{verbose} is not a valid verbosity level")
            log.info(f"INFO logging enabled")

    def get_db_connection_string(self, db):
        return (
            f"postgresql://{self.db_config[db]['user']}:{self.db_config[db]['password']}@"
            f"{self.db_config[db]['host']}:{self.db_config[db]['port']}"
            f"/{self.db_config[db]['name']}"
        )  # pragma: allowlist secret


class LocalConfig(BaseConfig):
    verbosity_levels = {0: "INFO", 1: "DEBUG", 2: "VERBOSE", 3: "DATA"}

    def data(self, msg, *args, **kwargs):
        if logging.getLogger().isEnabledFor(self.DATA):
            logging.log(self.DATA, msg)

    def custom_log_level(self):
        logging.addLevelName(self.VERBOSE, "VERBOSE")
        logging.Logger.verbose = self.verbose

        logging.addLevelName(self.DATA, "DATA")
        logging.Logger.data = self.data


def get_config(env="local"):
    if env == "local":
        config = LocalConfig()
    else:
        config = BaseConfig()
    return config
