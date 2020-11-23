import os
import logging


class BaseConfig:
    etl1_schema = "etl1"
    etl2_schema = "etl2"

    row_limit = 5

    VERBOSE = 5
    DATA = 2
    verbosity_levels = {0: "INFO", 1: "DEBUG", 2: "VERBOSE"}
    SAMPLE_PERCENTAGE = 1

    def verbose(self, msg, *args, **kwargs):
        if logging.getLogger().isEnabledFor(self.VERBOSE):
            logging.log(self.VERBOSE, msg)

    def custom_log_level(self):
        logging.addLevelName(self.VERBOSE, "VERBOSE")
        logging.Logger.verbose = self.verbose


class LocalConfig(BaseConfig):
    connection_string = f"postgresql://casrec:casrec@localhost:6666/casrecmigration"  # pragma: allowlist secret
    verbosity_levels = {0: "INFO", 1: "DEBUG", 2: "VERBOSE", 3: "DATA"}

    def data(self, msg, *args, **kwargs):
        if logging.getLogger().isEnabledFor(self.DATA):
            logging.log(self.DATA, msg)

    def custom_log_level(self):
        logging.addLevelName(self.VERBOSE, "VERBOSE")
        logging.Logger.verbose = self.verbose

        logging.addLevelName(self.DATA, "DATA")
        logging.Logger.data = self.data


class AWSConfig(BaseConfig):
    password = os.environ.get("DB_PASSWORD")
    db_host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    name = os.environ.get("DB_NAME")

    connection_string = f"postgresql://casrec:{password}@{db_host}:{port}/{name}"  # pragma: allowlist secret


def get_config(env="local"):
    if env == "local":
        config = LocalConfig()
    else:
        config = AWSConfig()
    return config
