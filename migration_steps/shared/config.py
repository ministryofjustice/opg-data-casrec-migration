import logging
import os
from pathlib import Path
from deprecated import deprecated
from dotenv import load_dotenv


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
        "pre_transform": "casrec_csv",
        "post_transform": "transform",
        "integration": "integration",
        "public": "public",
        "pre_migration": "staging",
    }

    row_limit = 5

    VERBOSE = 5
    DATA = 2
    verbosity_levels = {0: "INFO", 1: "DEBUG", 2: "VERBOSE"}

    def verbose(self, msg, *args, **kwargs):
        if logging.getLogger().isEnabledFor(self.VERBOSE):
            logging.log(self.VERBOSE, msg)

    @deprecated(
        version="1", reason="You should use custom_logger.setup_logging instead"
    )
    def custom_log_level(self):
        logging.addLevelName(self.VERBOSE, "VERBOSE")
        logging.Logger.verbose = self.verbose

    def get_db_connection_string(self, db):
        return (
            f"postgresql://{self.db_config[db]['user']}:{self.db_config[db]['password']}@"
            f"{self.db_config[db]['host']}:{self.db_config[db]['port']}"
            f"/{self.db_config[db]['name']}"
        )  # pragma: allowlist secret

    DEFAULT_CHUNK_SIZE = 20000

    ENABLED_ENTITIES = {
        "clients": True,
        "cases": True,
        "bonds": False,
        "supervision_level": False,
        "deputies": True,
        "events": False,
        "finance": False,
        "remarks": False,
        "reporting": False,
        "tasks": False,
        "teams": False,
        "visits": False,
        "warnings": False,
        "additional_data": False,
        "death": True,
    }


class LocalConfig(BaseConfig):
    verbosity_levels = {0: "INFO", 1: "DEBUG", 2: "VERBOSE", 3: "DATA"}
    SAMPLE_PERCENTAGE = 10
    MIN_PERCENTAGE_FIELDS_TESTED = 96  # 100 would be better but not there yet!

    def data(self, msg, *args, **kwargs):
        if logging.getLogger().isEnabledFor(self.DATA):
            logging.log(self.DATA, msg)

    @deprecated(
        version="1", reason="You should use custom_logger.setup_logging instead"
    )
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
